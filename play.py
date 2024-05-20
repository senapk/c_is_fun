#!/usr/bin/env python3

import argparse
import subprocess
import re
from typing import List, Tuple, Optional, Dict
import enum
import json
import os

baseurl = "https://github.com/senapk/c_is_fun/blob/main/graph/Readme.md"

class Color(enum.Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    RESET = 8
    BOLD = 9
    ULINE = 10

class Colored:
    enabled = True

    __map = {
        Color.RED: '\u001b[31m',
        Color.GREEN: '\u001b[32m',
        Color.YELLOW: '\u001b[33m',
        Color.BLUE: '\u001b[34m',
        Color.MAGENTA: '\u001b[35m',
        Color.CYAN: '\u001b[36m',
        Color.WHITE: '\u001b[37m',
        Color.RESET: '\u001b[0m',
        Color.BOLD: '\u001b[1m',
        Color.ULINE: '\u001b[4m'
    }

    @staticmethod
    def paint(text: str, color: Color, color2: Optional[Color] = None) -> str:
        if not Colored.enabled:
            return text
        return (Colored.__map[color] + ("" if color2 is None else Colored.__map[color2])
                + text + Colored.__map[Color.RESET])

    @staticmethod
    def green(text: str) -> str:
        return Colored.paint(text, Color.GREEN)
    
    @staticmethod
    def red(text: str) -> str:
        return Colored.paint(text, Color.RED)

    @staticmethod
    def cyan(text: str) -> str:
        return Colored.paint(text, Color.CYAN)

    @staticmethod
    def magenta(text: str) -> str:
        return Colored.paint(text, Color.MAGENTA)

    @staticmethod
    def yellow(text: str) -> str:
        return Colored.paint(text, Color.YELLOW)
    
    @staticmethod
    def blue(text: str) -> str:
        return Colored.paint(text, Color.BLUE)

    @staticmethod
    def ljust(text: str, width: int) -> str:
        return text + ' ' * (width - Colored.len(text))

    @staticmethod
    def center(text: str, width: int, filler: str) -> str:
        return filler * ((width - Colored.len(text)) // 2) + text + filler * ((width - Colored.len(text) + 1) // 2)

    @staticmethod
    def remove_colors(text: str) -> str:
        for color in Colored.__map.values():
            text = text.replace(color, '')
        return text

    @staticmethod
    def len(text):
        return len(Colored.remove_colors(text))

class Task:
    def __init__(self):
        self.line_number = 0
        self.line = ""
        self.key = ""
        self.coding = False
        self.remove_tko = False
        self.done = False
        self.skills = []
        self.title = ""
        self.link = ""

    def __str__(self):
        return f"{self.line_number} : {self.key} : {self.done} : {self.title} : {self.skills} : {self.link}"

    @staticmethod
    def parse_titulo_link_html(line):
        # Regex para extrair o título e o link
        titulo_link_regex = r'\s*- \[.\].*\[(.*?)\](\(.+?\))'
        titulo_link_match = re.search(titulo_link_regex, line)

        # Regex para extrair as tags
        html_regex = r'<!--\s*(.*?)\s*-->'
        html_match = re.search(html_regex, line)

        # Inicializa as variáveis de título, link e html
        titulo = None
        link = None
        html = []

        # Extrai título e link
        if titulo_link_match:
            titulo = titulo_link_match.group(1).strip()
            link = titulo_link_match.group(2).strip('()')

        # Extrai html
        if html_match:
            html_raw = html_match.group(1).strip()
            html = [tag.strip() for tag in html_raw.split()]

        return titulo, link, html

    # coding tasks
    def set_key_from_title(self, titulo, html):
        title_key = titulo.split("@")[1]
        title_key = title_key.split(" ")[0]
        title_key = title_key.split(":")[0]
        title_key = title_key.split("/")[0]
        self.key = title_key
        self.skills = html
        self.coding = True

    # non coding tasks
    def set_key_from_html(self, titulo, html):
            html_key = [t for t in html if t.startswith("@")][0]
            html_key = html_key.split("@")[1]
            self.key = html_key
            self.coding = False
            self.skills = [t[2:] for t in html if t.startswith("s:")]

    def parse_task(self, line, line_num):
        if line == "":
            return False
        line = line.lstrip()
        if not line.startswith("- [ ]") and not line.startswith("- [x]"):
            return False

        titulo, link, html = Task.parse_titulo_link_html(line)

        if titulo is None:
            print(line)
            print("Erro ao extrair título")
            return False

        self.line = line
        self.line_number = line_num
        self.title = titulo
        self.link = link

        try:
            self.set_key_from_title(titulo, html)
            return True
        except:
            pass
        try:
            self.set_key_from_html(titulo, html)
            return True
        except:
            pass

        return False

class Quest:
    def __init__(self):
        self.line_number = 0
        self.line = ""
        self.key = ""
        self.title = ""
        self.mdlink = ""
        self.tasks = []
        self.skills = []
        self.requires = []
        self.requires_ptr = []
        self.type = "main"

    def __str__(self):
        return f"linha={self.line_number} : {self.key} : {self.title} : {self.skills} : {self.requires} : {self.mdlink} : {[t.key for t in self.tasks]}"

    def is_complete(self):
        return all([t.done for t in self.tasks])
    
    def is_reachable(self, cache):
        if self.key in cache:
            return cache[self.key]

        if len(self.requires_ptr) == 0:
            cache[self.key] = True
            return True
        cache[self.key] = all([r.is_complete() and r.is_reachable(cache) for r in self.requires_ptr])
        return cache[self.key]

    def parse_quest(self, line, line_num):
        pattern = r'^\s*#+\s*(.*?)\s*<!--\s*(.*?)\s*-->\s*$'
        match = re.match(pattern, line)
        titulo = None
        tags = []

        if match:
            titulo = match.group(1).strip()
            tags_raw = match.group(2).strip()
            tags = [tag.strip() for tag in tags_raw.split()]

        try:
            key = [t[1:] for t in tags if t.startswith("@")][0]
            self.line = line
            self.line_number = line_num
            self.title = titulo
            self.skills = [t[2:] for t in tags if t.startswith("s:")]
            self.requires = [t[2:] for t in tags if t.startswith("r:")]
            type = [t for t in tags if t.startswith("t:")]
            if len(type) > 0:
                self.type = type[0][2:]
            self.key = key
            return True
        except:
            return False

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

class Rep:
    def __init__(self):
        self.from_file = ""
        self.from_url = ""
        self.active_quests: List[str] = []
        self.done_tasks: List[str] = []

    def get_file(self):
        if self.from_file != "":
            return self.from_file
        return self.from_url
    
    def __str__(self):
        return f"from_file={self.from_file} : from_url={self.from_url} : active_quests={self.active_quests} : done_tasks={self.done_tasks}"

class Save:
    def __init__(self, file: str = ""):
        self.default_track = ""
        self.reps: Dict[str:Rep] = {}
        self.file = file

    def save_to_json(self):
        with open(self.file, "w") as f:
            json.dump(self, f, default=lambda o: o.__dict__, indent=4)

    def set_track_file(self, track, file):
        if track not in self.reps:
            self.reps[track] = Rep()
        self.reps[track].from_file = file

    def has_track_source(self, track):
        if self.reps[track].from_file != "":
            return True
        if self.reps[track].from_url != "":
            return True
        return False


    def load_from_json(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                data = json.load(f)
                self.default_track = data["default_track"]
                self.reps = {}
                for k, v in data["reps"].items():
                    rep = Rep()
                    rep.from_file = v["from_file"]
                    rep.from_url = v["from_url"]
                    rep.active_quests = v["active_quests"]
                    rep.done_tasks = v["done_tasks"]
                    self.reps[k] = rep
            

    def __str__(self):
        return f"Reps: {self.reps}"

class Game:

    def load_quest(self, line, line_num):
        quest = Quest()
        if not quest.parse_quest(line, line_num + 1):
            return (False, None)
        if quest.key in self.quests:
            print(f"Quest {quest.key} já existe")
            print(quest)
            print(self.quests[quest.key])
            exit(1)
        self.quests[quest.key] = quest
        return (True, quest)

    def load_task(self, line, line_num, last_quest):
        task = Task()
        if not task.parse_task(line, line_num + 1):
            return False
        if last_quest is None:
            print(f"Task {task.key} não está dentro de uma quest")
            print(task)
            exit(1)
        last_quest.tasks.append(task)
        if task.key in self.tasks:
            print(f"Task {task.key} já existe")
            print(task)
            print(self.tasks[task.key])
            exit(1)
        self.tasks[task.key] = task
        return True
    
    # Verificar se todas as quests requeridas existem e adiciona o ponteiro
    # Verifica se todas as quests tem tarefas
    def validate_requirements(self):
        for q in self.quests.values():
            if len(q.tasks) == 0:
                print(f"Quest {q.key} não tem tarefas")
                exit(1)

        for q in self.quests.values():
            for r in q.requires:
                if r in self.quests:
                    q.requires_ptr.append(self.quests[r])
                else:
                    print(f"Quest\n{str(q)}\nrequer {r} que não existe")
                    exit(1)

        #check if there is a cycle

    def check_cycle(self):
        def dfs(q, visited):
            if len(visited) > 0:
                if visited[0] == q.key:
                    print(f"Cycle detected: {visited}")
                    exit(1)
            if q.key in visited:
                return
            visited.append(q.key)
            for r in q.requires_ptr:
                dfs(r, visited)

        for q in self.quests.values():
            visited = []
            dfs(q, visited)

    def __init__(self):
        self.quests = {}
        self.tasks = {}

    def parse_file(self, file):
        lines = open(file).read().split("\n")
        last_quest = None
        for index, line in enumerate(lines):
            found, quest = self.load_quest(line, index)
            if found:
                last_quest = quest
            else:
                self.load_task(line, index, last_quest)
        self.validate_requirements()

    def get_reachable_quests(self):
        # cache needs to be reseted before each call
        cache = {}
        return [q for q in self.quests.values() if q.is_reachable(cache)]


    def show_quests(self):
        print(f"Quests de Entrada: {[q.key for q in self.quests.values() if len(q.requires) == 0]}")
        print(f"Total de quests: {len(self.quests)}")
        print("\n".join([str(q) for q in self.quests.values()]))



class Play:
    def __init__(self, track, game: Game, save: Save):
        
        self.save = save
        self.rep = save.reps[track]
        self.game = game
        self.tasks = []
        self.quests = {} # option:quest
        self.active = set(self.rep.active_quests)
        for t in game.tasks.values():
            if t.key in self.rep.done_tasks:
                t.done = True


    def save_to_json(self):
        self.rep.active_quests = list(self.active)
        self.rep.done_tasks = [t.key for t in self.game.tasks.values() if t.done]
        self.save.save_to_json()

    def update_reachable(self):
        quests = self.game.get_reachable_quests()
        reach_keys = [q.key for q in quests]
        menu_keys = [q.key for q in self.quests.values()]

        for key in menu_keys:
            if not key in reach_keys:
                self.quests = {}
                break
        
        if len(self.quests) == 0:
            index_letter = 0
            for q in quests:
                letter = chr(ord("A") + index_letter)
                self.quests[letter] = q
                index_letter += 1
        else:
            index_letter = len(self.quests.keys())
            for q in quests:
                if not q.key in menu_keys:
                    letter = chr(ord("A") + index_letter)
                    self.quests[letter] = q
                    index_letter += 1

        self.active = set([k for k in self.active if k in reach_keys])

        # if len(self.quests.values()) == 1:
        #     for q in self.quests.values():
        #         self.active.add(q.key)


    def show_tasks(self):
        self.tasks = []
        index = 0

        self.update_reachable()

        for key in sorted(self.quests.keys()):
            q = self.quests[key]
            resume = ""
            opening = "⮞"
            if q.key in self.active:
                opening = "⮟"
            done = len([t for t in q.tasks if t.done])
            size = len(q.tasks)
            text = f"[{done}/{size}]"
            if done == size:
                resume = Colored.green(text)
            else:
                resume = Colored.yellow(text)

            print(f"{opening} {Colored.blue(key) if q.type == "main" else Colored.magenta(key)} {resume} {q.title}")
            if q.key not in self.active:
                continue
            for t in q.tasks:
                print(f"   {str(index).rjust(2, "0")} [{"x" if t.done else " "}] {t.title} {t.link}")
                index += 1
                self.tasks.append(t)

    @staticmethod
    def get_num_num(s):
        pattern = r'^(\d+)-(\d+)$'
        match = re.match(pattern, s)
        if match:
            return int(match.group(1)), int(match.group(2))
        else:
            return (None, None)

    @staticmethod
    def get_letter_letter(s):
        pattern = r'^([A-Z])-([A-Z])$'
        match = re.match(pattern, s)
        if match:
            return match.group(1), match.group(2)
        pattern = r'^([a-z])-([a-z])$'
        match = re.match(pattern, s)
        if match:
            return match.group(1), match.group(2)
        return (None, None)

    def expand_range(self, actions):
        expand = []
        for t in actions:
            (start_number, end_number) = self.get_num_num(t)
            (start_letter, end_letter) = self.get_letter_letter(t)
            if start_number is not None:
                expand += list(range(start_number, end_number + 1))
            elif start_letter is not None:
                expand += [chr(i) for i in range(ord(start_letter), ord(end_letter) + 1)]
            else:
                expand.append(t)
        return expand

    def take_actions(self, actions):
        for t in actions:
            if t == "?":
                subprocess.run("clear")
                self.show_help()
            if t == "<":
                self.active = set()
            if t == ">":
                self.update_reachable()
                self.active = set([q.key for q in self.quests.values()])
            try: # number
                t = int(t)
                if t >= 0 and t < len(self.tasks):
                    self.tasks[t].done = not self.tasks[t].done
            except: # letter
                t = t.upper()
                if t in self.quests:
                    key = self.quests[t].key
                    if key not in self.active:
                        self.active.add(key)
                    else:
                        self.active.remove(key)
                else:
                    print(f"{t} não processado")

    def show_help(self):
        print("Digite os números ou intervalo para as tarefas que deseja (marcar/desmarcar), exemplo:")
        print(Colored.green("$ ") + "1 2 5-6")
        print("Digite as letras ou intervalo para as quests que deseja (expandir/colapsar), exemplo:")
        print(Colored.green("$ ") + "a c d-g")
        print("Digite > para expandir todas as quests")
        print(Colored.green("$ ") + ">")
        print("Digite < para colapsar todas as quests")
        print(Colored.green("$ ") + "<")
        print("Digite ? para mostrar a ajuda")
        print(Colored.green("$ ") + "?")
        print("Digite ! para sair")
        print(Colored.green("$ ") + "!")
        print("Digite enter para continuar")
        input()

    def play(self):
        while True:
            subprocess.run("clear")
            print(f"\nDigite {Colored.green("números")} para (marcar/desmarcar), {Colored.green("letras")} para (expandir/colapsar), {Colored.green("!")} para sair ou {Colored.green("?")} para ajuda.\n")
            self.show_tasks()
            print(f"\n{Colored.green("$")} ", end="")
            actions = input().split(" ")
            if "!" in actions:
                break
            actions = self.expand_range(actions)
            self.take_actions(actions)
            self.save_to_json()


def create_diag(quests, output, colors = None):
    saida = []
    saida.append(f"@startuml {output}")
    saida.append("skinparam defaultFontName Hasklig")
    # saida.append("skinparam defaulttextalignment left")

    # links  = " [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/full_data.svg full_data]]"
    # links += " [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/main_only.svg main_only]]"
    # links += " [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/main_side.svg main_side]]"
    # links += " [[https://raw.githubusercontent.com/senapk/c_is_fun/main/graph/main_game.svg main_game]]"

    # saida.append("header")
    # saida.append("C is Fun links: " + links)
    # saida.append("end header")
    #saida.append("left to right direction")

    for q in quests.values():
        token = "-->"
        for r in q.requires_ptr:
            color_r = "lime" if r.type == "main" else "yellow"
            color_q = "lime" if q.type == "main" else "yellow"
            saida.append(f"{r.key} #{color_r} {token} {q.key} #{color_q}")


    saida.append(f"{list(quests.values())[-1].key} --> (*)")

    # skills = {}
    # for e in entries:
    #     for s, v in e.skills:
    #         if s not in skills:
    #             skills[s] = v
    #         else:
    #             skills[s] += v

    # saida.append("legend bottom left")

    # for s in skills:
    #     name = s.rjust(7, ".")
    #     print(name)
    #     saida.append(f"  {name}: {skills[s]}")
    # saida.append("end legend")

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
    parse.add_argument("--track", "-t", type=str, help="Trilha a seguir")
    parse.add_argument("--file", "-f", type=str, help="File to parse course plan")
    parse.add_argument("--config", "-c", type=str, help="File to save config")
    parse.add_argument("--output", type=str, help="Output file")
    parse.add_argument("--colors", type=str, nargs="*", help="Colors to use in the graph")
    parse.add_argument("--play", "-p", action="store_true", help="Play the game")
    parse.add_argument("--quests", "-q", action="store_true", help="Show quests")
    args = parse.parse_args()

    if args.config is None:
        args.config = "save.json"

    save = Save(args.config)
    save.load_from_json()
    if args.track is not None and args.file is not None:
        save.set_track_file(args.track, args.file)
        save.save_to_json()

    if args.track is None:
        args.track = save.default_track

    if args.track == "":
        print("Você precisa adicionar uma trilha para seguir")
        return

    if not save.has_track_source(args.track):
        print(f"Trilha {args.track} não definida")
        return
    
    game = Game()
    game.parse_file(save.reps[args.track].get_file())
    create_diag(game.quests, "graph", None)
    game.check_cycle()


    play = Play(args.track, game, save)
    play.play()

    if args.quests:
        finished_quests = [q for q in game.quests.values() if q.is_complete()]
        print(f"Quests completas: {[str(q.key) for q in finished_quests]}")
        reachable_quests = game.get_reachable_quests()
        print(f"Quests alcançáveis: {[str(q.key) for q in reachable_quests if not q.is_complete()]}")
        return

if __name__ == "__main__":
    main()
