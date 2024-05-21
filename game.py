#!/usr/bin/env python3

import argparse
import subprocess
import re
from typing import List, Tuple, Optional, Dict
import enum
import json
import os
import shutil

baseurl = "https://github.com/senapk/c_is_fun/blob/main/"


class Color:
  map = {
      "red": '\u001b[31m',
      "green": '\u001b[32m',
      "yellow": '\u001b[33m',
      "blue": '\u001b[34m',
      "magenta": '\u001b[35m',
      "cyan": '\u001b[36m',
      "white": '\u001b[37m',
      "reset": '\u001b[0m',
      "bold": '\u001b[1m',
      "uline": '\u001b[4m'
  }

  @staticmethod
  def ljust(text: str, width: int) -> str:
    return text + ' ' * (width - Color.len(text))

  @staticmethod
  def center(text: str, width: int, filler: str) -> str:
    return filler * ((width - Color.len(text)) // 2) + text + filler * (
        (width - Color.len(text) + 1) // 2)

  @staticmethod
  def remove_colors(text: str) -> str:
    for color in Color.__map.values():
      text = text.replace(color, '')
    return text

  @staticmethod
  def len(text):
    return len(Color.remove_colors(text))

def colour(text: str, color: str="green", color2: Optional[str] = None) -> str:
  return (Color.map[color] + ("" if color2 is None else Color.map[color2]) + text + Color.map["reset"])

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
    titulo_link_regex = r'\s*-.*\[(.*?)\](\(.+?\))'
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

  def process_link(self):
    if self.link.startswith("http"):
      return
    if self.link.startswith("./"):
      self.link = self.link[2:]
    self.link = baseurl + self.link

  def parse_task(self, line, line_num):
    if line == "":
      return False
    line = line.lstrip()
    # if not line.startswith("- [ ]") and not line.startswith("- [x]"):
    #   return False

    titulo, link, html = Task.parse_titulo_link_html(line)

    if titulo is None:
      print(line)
      print("Erro ao extrair título")
      return False

    self.line = line
    self.line_number = line_num
    self.title = titulo
    self.link = link

    self.process_link()

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
    cache[self.key] = all(
        [r.is_complete() and r.is_reachable(cache) for r in self.requires_ptr])
    return cache[self.key]

  def parse_quest(self, line, line_num):
    pattern = r'^#+\s*(.*?)<!--\s*(.*?)\s*-->\s*$'
    match = re.match(pattern, line)
    titulo = None
    tags = []

    if match:
      titulo = match.group(1)
      tags_raw = match.group(2).strip()
      tags = [tag.strip() for tag in tags_raw.split()]

    try:
      key = [t[1:] for t in tags if t.startswith("@")][0]
      self.line = line
      self.line_number = line_num
      self.title = titulo
      self.skills = [t[2:] for t in tags if t.startswith("s:")]
      self.requires = [t[2:] for t in tags if t.startswith("r:")]
      self.mdlink = baseurl + "ReadmePlan.md#" + get_md_link(titulo)
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
  if title is None:
    return ""
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
    self.show_url = False
    self.show_all = False


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
    self.reps[track].from_file = os.path.abspath(file)
    self.default_track = track

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
          rep.show_url = v["show_url"]
          rep.show_all = v["show_all"]
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
    print( f"Quests de Entrada: {[q.key for q in self.quests.values() if len(q.requires) == 0]}" )
    print(f"Total de quests: {len(self.quests)}")
    print("\n".join([str(q) for q in self.quests.values()]))


class Play:

  def __init__(self, track, game: Game, save: Save):
    self.save = save
    self.rep = save.reps[track]
    self.show_url = self.rep.show_url
    self.show_all = self.rep.show_all
    self.game = game
    self.tasks = []
    self.quests = {}  # option:quest
    self.active = set(self.rep.active_quests)
    self.term_limit = 130

    for t in game.tasks.values():
      if t.key in self.rep.done_tasks:
        t.done = True

  def save_to_json(self):
    self.rep.active_quests = list(self.active)
    self.rep.done_tasks = [t.key for t in self.game.tasks.values() if t.done]
    self.rep.show_url = self.show_url
    self.rep.show_all = self.show_all
    self.save.save_to_json()

  @staticmethod
  def calc_letter(index_letter):
    unit = index_letter % 26
    ten = index_letter // 26
    if ten == 0:
      return chr(ord("A") + unit)
    return chr(ord("A") + ten - 1) + chr(ord("A") + unit)

  @staticmethod
  def calc_index(letter):
    letter = letter.upper()
    if len(letter) == 1:
      return ord(letter) - ord("A")
    return (ord(letter[0]) - ord("A") + 1) * 26 + (ord(letter[1]) - ord("A"))

  def update_reachable(self):
    quests = self.game.get_reachable_quests()
    reach_keys = []
    reach_keys = [q.key for q in quests]
    menu_keys = [q.key for q in self.quests.values()]

    for key in menu_keys:
      if key not in reach_keys:
        self.quests = {}
        break

    if len(self.quests) == 0:
      index_letter = 0
      for q in quests:
        letter = self.calc_letter(index_letter)
        self.quests[letter] = q
        index_letter += 1
    else:
      index_letter = len(self.quests.keys())
      for q in quests:
        if q.key not in menu_keys:
          letter = self.calc_letter(index_letter)
          self.quests[letter] = q
          index_letter += 1

    self.active = set([k for k in self.active if k in reach_keys])

    # if len(self.quests.values()) == 1:
    #     for q in self.quests.values():
    #         self.active.add(q.key)


  def calculate_pad(self):
    titles = []
    keys = self.quests.keys()
    for key in keys:
      q = self.quests[key]
      titles.append(q.title)
      if q.key not in self.active:
        continue
      for t in q.tasks:
        titles.append(t.title)
    max_title = 10
    if (len(titles) > 0):
      max_title = max([len(t) for t in titles])
    return max_title


  def print_quest(self, entry, q, max_title, term_size):
    resume = ""
    opening = "➡️"
    if q.key in self.active:
      opening = "⬇️"
    done = len([t for t in q.tasks if t.done])
    size = len(q.tasks)
    text = f"[{done}/{size}]"
    space = " " if len(entry) == 1 else ""
    if done == size:
      resume = colour(text, "green")
    else:
      resume = colour(text, "yellow")
    entry = colour(entry, "blue") if q.type == "main" else colour(entry, "magenta")
    qlink = ""
    if self.show_url:
      if term_size > self.term_limit:
        qlink = " " + colour(q.mdlink, "cyan")
      else:
        qlink = "\n      " + colour(q.mdlink, "cyan")
    if not self.show_all and done == size:
      return
    print(f"{opening} {entry}{space}{resume} {q.title.ljust(max_title)}{qlink}")

  def print_task(self, t, max_title, index, term_size):
    vindex = str(index).rjust(2, "0")
    vdone = "x" if t.done else " "
    vlink = ""
    if self.show_url:
      if t.key in t.title:
        vlink = colour(t.link, "red")
      else:
        vlink = colour(t.link, "yellow")
      if term_size > self.term_limit:
        vlink = " " + vlink
      else:
        vlink = "\n      " + vlink
    print(f"   {vindex} [{vdone}] {t.title.ljust(max_title)}{vlink}")

  def sort_keys(self, keys):
    single = [k for k in keys if len(k) == 1]
    double = [k for k in keys if len(k) == 2]
    return sorted(single) + sorted(double)

  def show_tasks(self):
    term_size = shutil.get_terminal_size().columns
    self.tasks = []

    self.update_reachable()
    max_title = self.calculate_pad()
    index = 0
    for entry in self.sort_keys(self.quests.keys()):
      q = self.quests[entry]
      self.print_quest(entry, q, max_title, term_size)
      if q.key not in self.active:
        continue
      if not self.show_all and q.is_complete():
        continue
      for t in q.tasks:
        self.print_task(t, max_title, index, term_size)
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
    pattern =r'([a-zA-Z]+)-([a-zA-Z]+)'
    match = re.match(pattern, s)
    if match:
      print(match.group(1), match.group(2))
      return match.group(1), match.group(2)
    return (None, None)

  def expand_range(self, line):
    line = line.replace(" - ", "-")
    actions = line.split()

    expand = []
    for t in actions:
      (start_number, end_number) = self.get_num_num(t)
      (start_letter, end_letter) = self.get_letter_letter(t)
      if start_number is not None and end_number is not None:
        expand += list(range(start_number, end_number + 1))
      elif start_letter is not None and end_letter is not None:
        start_index = self.calc_index(start_letter)
        end_index = self.calc_index(end_letter)
        print(start_index, end_index)
        expand += [self.calc_letter(i) for i in range(start_index, end_index + 1)]
      else:
        expand.append(t)
    return expand

  def take_actions(self, actions):
    for t in actions:
      if t == ":h" or t == ":help" or t == "?":
        subprocess.run("clear")
        self.show_help()
      elif t == ":u" or t == ":url":
        self.show_url = not self.show_url
      elif t == ":a" or t == ":all":
        self.show_all = not self.show_all
      elif t == "<":
        self.active = set()
      elif t == ">":
        self.update_reachable()
        self.active = set([q.key for q in self.quests.values()])
      else:
        try:  # number
          t = int(t)
          if t >= 0 and t < len(self.tasks):
            self.tasks[t].done = not self.tasks[t].done
        except:  # letter
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
    print("Digite os números ou intervalo das tarefas para (marcar/desmarcar), exemplo:")
    print(colour("$ ", "green") + "1 2 5-6")
    print("Digite as letras ou intervalo das quests para (expandir/colapsar), exemplo:")
    print(colour("$ ", "green") + "a c d-g")
    print("Digite > para expandir todas as quests")
    print(colour("$ ", "green") + ">")
    print("Digite < para colapsar todas as quests")
    print(colour("$ ", "green") + "<")
    print("Digite :a ou :all para mostrar/esconder as quests completas")
    print(colour("$ ", "green") + ":all")
    print("Digite :u ou :url para mostrar/esconder as urls")
    print(colour("$ ", "green") + ":url")
    print("Digite :h ou :help para mostrar a ajuda")
    print(colour("$ ", "green") + ":h")
    print("Digite :q ou :quit para sair")
    print(colour("$ ", "green") + ":q")
    print("Digite enter para continuar")
    input()

  def play(self):
    while True:
      subprocess.run("clear")
      vnum = colour("números") + "(marcar)"
      vlet = colour("letras") + "(expandir)"
      vfold  = colour("<") + " ou " + colour(">") + "(expandir todas)"
      vall   = colour(":a", "cyan") + colour("ll") + ("[x]" if self.show_all else "[ ]")
      vurl   = colour(":u", "cyan") + colour("rl") + ("[x]" if self.show_url else "[ ]")
      vhelp  = colour(":h", "cyan") + colour("elp")
      vclose = colour(":q", "cyan") + colour("uit")
      print(f"Digite: {vnum}, {vlet}, {vfold}, {vall}, {vurl}, {vhelp} ou {vclose}.")
      self.show_tasks()
      print("\n" + colour("$") + " ", end="")
      line = input()
      if ":q" in line or ":quit" in line:
        break
      actions = self.expand_range(line)
      self.take_actions(actions)
      self.save_to_json()


def create_diag(quests, output, colors=None):
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
  parse.add_argument("--file",
                     "-f",
                     type=str,
                     help="File to parse course plan")
  parse.add_argument("--config", "-c", type=str, help="File to save config")
  parse.add_argument("--output", type=str, help="Output file")
  parse.add_argument("--colors",
                     type=str,
                     nargs="*",
                     help="Colors to use in the graph")
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
  else:
    save.default_track = args.track
    save.save_to_json()

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
