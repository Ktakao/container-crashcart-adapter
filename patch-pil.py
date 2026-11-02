import marshal
import shutil
import sys
import types
import zipfile

REPLACEMENTS = {
    (None, "fromstring"): "def fromstring(*args, **kw):\n    return frombytes(*args, **kw)\n",
    ("Image", "fromstring"): "def fromstring(self, *args, **kw):\n    return self.frombytes(*args, **kw)\n",
    ("Image", "tostring"): "def tostring(self, *args, **kw):\n    return self.tobytes(*args, **kw)\n",
}


def function_code(source):
    module = compile(source, "<patch>", "exec")
    return [c for c in module.co_consts if isinstance(c, types.CodeType)][0]


def rebuild(code, consts):
    return types.CodeType(
        code.co_argcount, code.co_nlocals, code.co_stacksize, code.co_flags,
        code.co_code, tuple(consts), code.co_names, code.co_varnames,
        code.co_filename, code.co_name, code.co_firstlineno, code.co_lnotab,
        code.co_freevars, code.co_cellvars)


def patch(code, scope, done):
    consts = []
    for const in code.co_consts:
        if isinstance(const, types.CodeType):
            key = (scope, const.co_name)
            if key in REPLACEMENTS and any("has been removed" in str(c) for c in const.co_consts):
                const = function_code(REPLACEMENTS[key])
                done.append(key)
            else:
                const = patch(const, const.co_name, done)
        consts.append(const)
    return rebuild(code, consts)


def main(zip_path):
    name = "PIL/Image.pyc"
    with zipfile.ZipFile(zip_path) as zf:
        data = zf.read(name)
        infos = zf.infolist()
        contents = dict((i.filename, zf.read(i.filename)) for i in infos)
    done = []
    code = patch(marshal.loads(data[8:]), None, done)
    if sorted(done) != sorted(REPLACEMENTS):
        sys.exit("unexpected PIL/Image.pyc layout, patched: %r" % done)
    contents[name] = data[:8] + marshal.dumps(code)
    tmp = zip_path + ".tmp"
    with zipfile.ZipFile(tmp, "w") as out:
        for info in infos:
            out.writestr(info, contents[info.filename])
    shutil.move(tmp, zip_path)
    print("patched %s in %s" % (name, zip_path))


if __name__ == "__main__":
    main(sys.argv[1])
