#!/bin/bash
set -eu

# Search for the .deb file recursively in /app
deb_file=$(find /app -name "*.deb" | grep "X64" | head -n 1)
[ -z "${deb_file}" ] \
  && deb_file=$(find /app -name "*.deb" | head -n 1)

if [ -z "${deb_file}" ]; then
    echo "Error: No .deb file found in /app."
    exit 1
fi

echo "Found .deb package: ${deb_file}"
echo "Installing..."

# Install the package and dependencies
dpkg -i "${deb_file}" \
  || (apt update && apt install -f -y && dpkg -i "${deb_file}")

echo "Installation complete."

# Find the executable
package_name=$(dpkg -I "${deb_file}" | grep " Package:" | awk '{print $2}')
installed_files=$(dpkg -L "${package_name}")
executable=$(echo "${installed_files}" | grep -E "^/usr/bin/|^/bin/|^/opt/.*bin/" | head -n 1)

[ -z "${executable}" ] \
  && executable=$(
    echo "${installed_files}" |
      while read f; do
        if [ -x "${f}" ] && [ -f "${f}" ]; then
          echo "${f}"
          break
        fi
      done)

echo "Starting application: ${executable}"
exec "${executable}" "${@}"
