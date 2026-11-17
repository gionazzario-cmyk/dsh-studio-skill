#!/bin/zsh
set -e
DIR="${0:A:h}"
if [ ! -x "$DIR/ocr" ]; then swiftc -O "$DIR/ocr.swift" -o "$DIR/ocr"; fi
"$DIR/ocr" "$1"
