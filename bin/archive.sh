#!/bin/bash

current_path=$(pwd)
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" || echo "cd command failed" ; pwd -P )
cd "$parent_path" || echo "cd command failed"

cd ..
tar -czvf secrets.tar.gz secrets/*.env secrets/*.csv secrets/README.txt secrets/download.sh secrets/*.py
# -c: Create an archive.
# -z: Compress the archive with gzip.
# -v: Display progress in the terminal while creating the archive, also known as “verbose” mode. The v is always optional in these commands, but it’s helpful.
# -f: Allows you to specify the filename of the archive.

cd "$current_path" || echo "cd command failed"
