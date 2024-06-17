#!/usr/bin/env python3

import os

def compare_lines(line, file):
    for i in file:
        if i[6:] == line:
            return i
    return False

count = 1
changed = 0

lines = open('Readme.md').read().split("\n")
output = []

todolines = open('to-do.md').read().split("\n")

for line in lines:
    if line.startswith('###'):
        if not_modified := compare_lines(line, todolines):
            output.append(not_modified)
        else: 
            print(f"Changed line {count}: {line[:10]}[...]")
            changed += 1
            output.append(f"- [ ] {line}")

    count += 1

print(f"Finished. Changed {changed} " + ("line" if changed == 1 else "lines") + f" out of {count} lines")

with open('to-do.md', 'w') as f:
    f.write('\n'.join(output))
