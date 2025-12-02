#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <day-number>"
    exit 1
fi

uv run python -m doctest days/day$1/__init__.py -v