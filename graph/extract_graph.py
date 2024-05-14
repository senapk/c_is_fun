#!/usr/bin/env python3

class Entry:
    def __init__(self):
        self.label = ""
        self.main = False
        self.requires = []
        self.count = 0

    def format(self):
        color = "#lime" if self.main else "#pink"
        return f"\"{self.label} ({self.count})\" {color}"

    def __str__(self):
        return f"{self.label} {self.main} {self.requires} {self.count}"
    
def load_entries():
    entries = []
    lines = open("Readme.md").readlines()
    for line in lines:
        if line.startswith("- [ ] "):
            entries[-1].count += 1
            continue
        found = line.split("[](")
        if len(found) == 1:
            continue

        entry = Entry()
        data = found[1].split(")")[0]
        pieces = data.split(" ")
        label = ""
        if "t:main" in pieces:
            entry.main = True
        for piece in pieces:
            tag, value = piece.split(":")
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

entries = load_entries()
for e in entries:
    print(e)
create_diag(entries)





