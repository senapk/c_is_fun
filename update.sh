#!/bin/bash

./fix_numeracao_aulas.py
./mdpp.py Readme.md

# find all .md files, print them and run mdpp.py on them
find . -name "*.md" -print
find . -name "*.md"  -exec ./mdpp.py {} \;


