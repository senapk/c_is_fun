#!/usr/bin/env python3

import argparse

def rm_comments(title: str) -> str:
    if "<!--" in title and "-->" in title:
        title = title.split("<!--")[0] + title.split("-->")[1]
    return title

def get_md_link(title: str) -> str:
        # remove html comments
        title = rm_comments(title)

        if title is None:
            return ""
        title = title.lstrip(" #")
        title = title.lower()
        out = ''
        for c in title:
            if c == ' ' or c == '-':
                out += '-'
            elif c == '_':
                out += '_'
            elif c.isalnum():
                out += c
        return out

class Entry:
    def __init__(self):
        self.baseurl = ""
        self.line = ""
        self.label = ""
        self.main = False
        self.requires = []
        self.count = 0

    def format(self):
        color = "#lime" if self.main else "#pink"
        description = rm_comments(self.line)
        description = " ".join(description.split(" ")[1:])
        link = self.baseurl + "/" + get_md_link(description)
        return f"\"[[{link}{description} ({self.count})]]\" {color}"

    def __str__(self):
        return f"{self.label} {self.main} {self.requires} {self.count}"
    
def load_entries(file: str):
    entries = []
    lines = open(file).read().split("\n")
    for line in lines:
        if line.startswith("- [ ] "):
            if len(entries) == 0:
                continue
            entries[-1].count += 1
            continue

        if not "<!-- l:" in line:
            continue

        found = line.split("<!-- ")
        if len(found) == 1:
            continue

        entry = Entry()
        entry.line = line
        data = found[1].split(" -->")[0]
        pieces = data.split(" ")
        if "t:main" in pieces:
            entry.main = True
        for piece in pieces:
            try:
                tag, value = piece.split(":")
            except:
                print(line)
                exit(1)
            if tag == "l":
                entry.label = value
            if tag == "r":
                entry.requires.append(value)
        entries.append(entry)
    return entries

def create_diag(entries):
    map = {e.label: e for e in entries}
    saida = []
    saida.append("@startuml graph")

    #saida.append("skinparam defaulttextalignment center")
    #saida.append("left to right direction")

    for e in entries:
        token = "-->" if e.main else "-->"
        for r in e.requires:
            saida.append(f"{map[r].format()} {token} {map[e.label].format()}")

    main_list = [e for e in entries if e.main]

    saida.append(f"{map[main_list[-1].label].format()} -> (*)")
    saida.append("@enduml")

    open("graph.puml", "w").write("\n".join(saida))

def main():

    parse = argparse.ArgumentParser()
    parse.add_argument("file", help="File to extract graph")
    args = parse.parse_args()

    entries = load_entries(args.file)
    for e in entries:
        print(e)
    create_diag(entries)


if __name__ == "__main__":
    main()
