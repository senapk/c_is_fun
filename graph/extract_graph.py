#!/usr/bin/env python3

import argparse
import subprocess

baseurl = "https://github.com/senapk/c_is_fun/blob/main/graph/Readme.md"

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
        self.line = ""
        self.label = ""
        self.color = "yellow"
        self.requires = []
        self.skills = {} # skill: level
        self.count = 0

    def format(self):
        description = rm_comments(self.line)
        description = " ".join(description.split(" ")[1:])
        link = get_md_link(description)
        words = description.split("`")
        if len(words) > 2:
            description = "`".join(words[:-2])
        print(link)
        link = baseurl + "#" + link
        return f"\"[[{link} {description} ({self.count})]]\" #{self.color}"

    def __str__(self):
        return f"{self.label} #{self.color} {self.requires} {self.count}"
    
def extract_skills(line: str):
    try:
        pieces = line.split("`")[-2]
    except:
        print("Erro ao carregar os skills entre as crases")
        print(line)
        exit(1)
    skills = pieces.split(" ")
    out = []
    for s in skills:
        try:
            name, level = s.split(":")
        except:
            print("Erro ao carregar os skills no formato +skill:level")
            print(line)
            exit(1)
        out.append((name[1:], int(level)))
    return out

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
            if tag == "c":
                entry.color = value

        entry.skills = extract_skills(entry.line)

        entries.append(entry)

    return entries

def create_diag(entries, output, colors = None):
    map = {e.label: e for e in entries}
    saida = []
    saida.append(f"@startuml {output}")
    saida.append("skinparam defaultFontName Hasklig")

    saida.append("skinparam defaulttextalignment left")

    links  = " [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/full_data.svg full_data]]"
    links += " [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/main_only.svg main_only]]"
    links += " [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/main_side.svg main_side]]"
    links += " [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/main_game.svg main_game]]"

    saida.append("header")
    saida.append("C is Fun links: " + links)
    saida.append("end header")
    #saida.append("left to right direction")

    for e in entries:
        token = "-->"
        if colors is not None and not e.color in colors:
            continue
        for r in e.requires:
            saida.append(f"{map[r].format()} {token} {map[e.label].format()}")


    saida.append(f"{map[entries[-1].label].format()} -> (*)")

    skills = {}
    for e in entries:
        for s, v in e.skills:
            if s not in skills:
                skills[s] = v
            else:
                skills[s] += v

    saida.append("legend bottom left")

    for s in skills:
        name = s.rjust(7, ".")
        print(name)
        saida.append(f"  {name}: {skills[s]}")
    saida.append("end legend")

    # saida.append("note top right")
    # saida.append("    full_data: [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/full_data.svg LINK]]")
    # saida.append("    main_only: [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/main_only.svg LINK]]")
    # saida.append("    main_side: [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/main_side.svg LINK]]")
    # saida.append("    main_game: [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/main_game.svg LINK]]")
    # saida.append("end note")



    saida.append("@enduml")

    open(output + ".puml", "w").write("\n".join(saida))

def main():

    parse = argparse.ArgumentParser()
    parse.add_argument("--file", type=str, help="File to extract graph")
    parse.add_argument("--output", type=str, help="Output file")
    parse.add_argument("--colors", type=str, nargs="*", help="Colors to use in the graph")
    args = parse.parse_args()

    if args.file is None:
        args.file = "Readme.md"
    if args.output is None:
        args.output = "graph"

    entries = load_entries(args.file)
    for e in entries:
        print(e)
    create_diag(entries, args.output, args.colors)
    subprocess.run(["plantuml", "-tsvg", args.output + ".puml"])



if __name__ == "__main__":
    main()
