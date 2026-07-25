#!/bin/bash
set -e

cd "$(dirname "$0")"
python3 build_gallery.py

echo
echo "Gallery updated successfully."
