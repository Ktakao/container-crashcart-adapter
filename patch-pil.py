# Restore Image.fromstring()/tostring() in the PIL bundled with the vendor
# software. The vendor code still calls fromstring(), but the bundled
# Pillow 3.1.2 replaced it with a stub that only raises
# "fromstring() has been removed". Rewrite that stub (and the two matching
# methods) inside PIL/Image.pyc in library.zip so they delegate to
# frombytes()/tobytes(), which take the same arguments.
#
# Must run with Python 2.7: the .pyc is Python 2 bytecode.
# Usage: python2.7 patch-pil.py /path/to/library.zip
import marshal
import sys
import types
import zipfile

# (function name, positional argument count) -> replacement source.
# Argument count 0 is the module-level function, 1 is the Image method
# (its single positional argument is self).
FIX = {
    ("fromstring", 0): "def fromstring(*a, **k): return frombytes(*a, **k)",
    ("fromstring", 1): "def fromstring(self, *a, **k): return self.frombytes(*a, **k)",
    ("tostring", 1): "def tostring(self, *a, **k): return self.tobytes(*a, **k)",
}


def patch(code):
    # Walk the nested code objects (module -> class body -> methods) held in
    # co_consts and swap in the replacement where name and argcount match.
    consts = []
    for c in code.co_consts:
        if isinstance(c, types.CodeType):
            src = FIX.get((c.co_name, c.co_argcount))
            # compile() yields a module code object whose first constant is
            # the function's code object.
            c = compile(src, "", "exec").co_consts[0] if src else patch(c)
        consts.append(c)
    # Code objects are immutable and Python 2 has no code.replace(), so
    # rebuild one with the new constants and everything else unchanged.
    return types.CodeType(
        code.co_argcount, code.co_nlocals, code.co_stacksize, code.co_flags,
        code.co_code, tuple(consts), code.co_names, code.co_varnames,
        code.co_filename, code.co_name, code.co_firstlineno, code.co_lnotab,
        code.co_freevars, code.co_cellvars)


# zipfile cannot replace a single entry, so read every entry into memory and
# write the archive back out with PIL/Image.pyc swapped.
path = sys.argv[1]
with zipfile.ZipFile(path) as z:
    files = [(i, z.read(i.filename)) for i in z.infolist()]
with zipfile.ZipFile(path, "w") as z:
    for info, data in files:
        if info.filename == "PIL/Image.pyc":
            # The first 8 bytes are the magic number and timestamp; the rest
            # is the marshalled module code object.
            data = data[:8] + marshal.dumps(patch(marshal.loads(data[8:])))
        z.writestr(info, data)
