#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import re
import configparser
from typing import List, Optional
import urllib.request
import argparse
import json
from typing import Optional, List, Dict, Any
import tempfile
import subprocess
from subprocess import PIPE
from typing import List, Tuple, Any
import shutil
from enum import Enum
from typing import Optional
from typing import List, Optional, Tuple
import io
from typing import Tuple, Optional
import urllib.error
from typing import List
from shutil import which
from typing import List, Tuple, Optional, Dict
import math
from typing import Optional, Dict, List, Tuple
from typing import Dict, List
import sys



class Title:
    @staticmethod
    def extract_title(readme_file):
        title = open(readme_file).read().split("\n")[0]
        parts = title.split(" ")
        if parts[0].count("#") == len(parts[0]):
            del parts[0]
        title = " ".join(parts)
        return title

class RemoteCfg:
    def __init__(self, url: Optional[str] = None):
        self.user = ""
        self.repo = ""
        self.branch = ""
        self.folder = ""
        self.file = ""
        if url is not None:
            self.from_url(url)

    def from_url(self, url: str):
        if url.startswith("https://raw.githubusercontent.com/"):
            url = url.replace("https://raw.githubusercontent.com/", "")
            parts = url.split("/")
            self.user = parts[0]
            self.repo = parts[1]
            self.branch = parts[2]
            self.folder = "/".join(parts[3:-1])
            self.file = parts[-1]
        elif url.startswith("https://github.com/"):
            url = url.replace("https://github.com/", "")
            parts = url.split("/")
            self.user = parts[0]
            self.repo = parts[1]
            self.branch = parts[3]
            self.folder = "/".join(parts[4:-1])
            self.file = parts[-1]
        else:
            raise Exception("Invalid URL")

    def get_raw_url(self):
        return "https://raw.githubusercontent.com/" + self.user + "/" + self.repo + "/" + self.branch + "/" + self.folder + "/" + self.file

    def download_absolute(self, filename: str):
        try:
            [tempfile, __content] = urllib.request.urlretrieve(self.get_raw_url(), filename)
            content = ""
            try:
                content = open(tempfile, encoding="utf-8").read()
            except:
                content = open(tempfile).read()
            with open(filename, "w") as f:
                f.write(Absolute.relative_to_absolute(content, self))
        except urllib.error.HTTPError:
            print("Error downloading file", self.get_raw_url())
            return

    def __str__(self):
        return f"user: ({self.user}), repo: ({self.repo}), branch: ({self.branch}), folder: ({self.folder}), file: ({self.file})"

    def read(self, cfg_path: str):
        if not os.path.isfile(cfg_path):
            print("no remote.cfg found")

        config = configparser.ConfigParser()
        config.read(cfg_path)

        self.user   = config["DEFAULT"]["user"]
        self.repo   = config["DEFAULT"]["rep"]
        self.branch = config["DEFAULT"]["branch"]
        self.folder = config["DEFAULT"]["base"]
        self.tag    = config["DEFAULT"]["tag"]

    @staticmethod
    def search_cfg_path(source_dir) -> Optional[str]:
        # look for the remote.cfg file in the current folder
        # if not found, look for it in the parent folder
        # if not found, look for it in the parent's parent folder ...

        path = os.path.abspath(source_dir)
        while path != "/":
            cfg_path = os.path.join(path, "remote.cfg")
            if os.path.isfile(cfg_path):
                return cfg_path
            path = os.path.dirname(path)
        return None

class Absolute:

    # processa o conteúdo trocando os links locais para links absolutos utilizando a url remota
    @staticmethod
    def __replace_remote(content: str, remote_raw: str, remote_view: str, remote_folder: str) -> str:
        if content is None or content == "":
            return ""
        if not remote_raw.endswith("/"):
            remote_raw += "/"
        if not remote_view.endswith("/"):
            remote_view += "/"
        if not remote_folder.endswith("/"):
            remote_folder += "/"

        #trocando todas as imagens com link local
        regex = r"!\[(.*?)\]\((\s*?)([^#:\s]*?)(\s*?)\)"
        subst = "![\\1](" + remote_raw + "\\3)"
        result = re.sub(regex, subst, content, 0)


        regex = r"\[(.+?)\]\((\s*?)([^#:\s]*?)(\s*?/)\)"
        subst = "[\\1](" + remote_folder + "\\3)"
        result = re.sub(regex, subst, result, 0)

        #trocando todos os links locais cujo conteudo nao seja vazio
        regex = r"\[(.+?)\]\((\s*?)([^#:\s]*?)(\s*?)\)"
        subst = "[\\1](" + remote_view + "\\3)"
        result = re.sub(regex, subst, result, 0)

        return result

    @staticmethod
    def relative_to_absolute(content: str, cfg: RemoteCfg):
        user_repo = os.path.join(cfg.user, cfg.repo)
        remote_raw    = os.path.join("https://raw.githubusercontent.com", user_repo, cfg.branch , cfg.folder)
        remote_view    = os.path.join("https://github.com/", user_repo, "blob", cfg.branch, cfg.folder)
        remote_folder = os.path.join("https://github.com/", user_repo, "tree", cfg.branch, cfg.folder)
        return Absolute.__replace_remote(content, remote_raw, remote_view, remote_folder)

    @staticmethod
    def from_file(source_file, output_file, cfg: RemoteCfg, hook):
        content = open(source_file).read()
        content = Absolute.relative_to_absolute(content, cfg, hook)
        open(output_file, "w").write(content)
        
class RemoteMd:

    # @staticmethod
    # def insert_preamble(lines: List[str], online: str, tkodown: str) -> List[str]:

    #     text = "\n- Veja a versão online: [aqui.](" + online + ")\n"
    #     text += "- Para programar na sua máquina (local/virtual) use:\n"
    #     text += "  - `" + tkodown + "`\n"
    #     text += "- Se não tem o `tko`, instale pelo [LINK](https://github.com/senapk/tko#tko).\n\n---"

    #     lines.insert(1, text)

    #     return lines

    # @staticmethod
    # def insert_qxcode_preamble(cfg: RemoteCfg, content: str, hook) -> str:
    #     base_hook = os.path.join(cfg.base, hook)

    #     lines = content.split("\n")
    #     online_readme_link = os.path.join("https://github.com", cfg.user, cfg.repo, "blob", cfg.branch, base_hook, "Readme.md")
    #     tkodown = "tko down " + cfg.tag + " " + hook
    #     lines = RemoteMd.insert_preamble(lines, online_readme_link, tkodown)
    #     return "\n".join(lines)

    @staticmethod
    def run(remote_cfg: RemoteCfg, source: str, target: str, hook) -> bool:    
        content = open(source).read()
        content = Absolute.relative_to_absolute(content, remote_cfg, hook)
        open(target, "w").write(content)


class RepoSettings:
    def __init__(self):
        self.url: str = ""
        self.file: str = ""
        self.cache: str = ""
        self.quests: Dict[str, str] = {}
        self.tasks: Dict[str, str] = {}
        self.view: List[str] = ["done", "init", "link", "todo"]

    def get_file(self) -> str:
        # arquivo existe e é local
        if self.file != "" and os.path.exists(self.file) and self.url == "":
            return self.file
        
        # arquivo não existe e é remoto
        if self.url != "" and (self.file == "" or not os.path.exists(self.file)):
                with tempfile.NamedTemporaryFile(delete=False) as f:
                    filename = f.name
                    cfg = RemoteCfg(self.url)
                    cfg.download_absolute(filename)
                return filename

        # arquivo é local com url remota
        if self.file != "" and os.path.exists(self.file) and self.url != "":
            content = open(self.file).read()
            content = Absolute.relative_to_absolute(content, RemoteCfg(self.url))
            with tempfile.NamedTemporaryFile(delete=False) as f:
                filename = f.name
                f.write(content.encode("utf-8"))
            return filename

        raise ValueError("fail: file not found or invalid settings to download repository file")
        

    def set_file(self, file: str):
        self.file = os.path.abspath(file)
        return self

    def set_url(self, url: str):
        self.url = url
        return self

    def to_dict(self):
        return {
            "url": self.url,
            "file": self.file,
            "cache": self.cache,
            "quests": self.quests,
            "tasks": self.tasks,
            "view": self.view
        }
    
    def from_dict(self, data: Dict[str, Any]):
        self.url = data.get("url", "")
        self.file = data.get("file", "")
        self.cache = data.get("cache", "")
        self.quests = data.get("quests", {})
        self.tasks = data.get("tasks", {})
        self.view = data.get("view", [])
        return self

    def __str__(self) -> str:
        return (
            f"url: {self.url}\n"
            f"file: {self.file}\n"
            f"cache: {self.cache}\n"
            f"Quests: {self.quests}\n"
            f"Tasks: {self.tasks}\n"
            f"View: {self.view}\n"
        )

class LocalSettings:
    def __init__(self):
        self.lang: str = "ask"
        self.ascii: bool = False
        self.color: bool = True
        self.updown: bool = True
        self.sideto_min: int = 60

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lang": self.lang,
            "ascii": self.ascii,
            "color": self.color,
            "updown": self.updown,
            "sideto_min": self.sideto_min
        }
    
    def from_dict(self, data: Dict[str, Any]):
        self.lang = data.get("lang", "ask")
        self.ascii = data.get("ascii", False)
        self.color = data.get("color", True)
        self.updown = data.get("updown", True)
        self.sideto_min = data.get("sideto_min", 60)
        return self

    def __str__(self) -> str:
        return (
            f"Default Language: {self.lang}\n"
            f"Encoding Mode: {'ASCII' if self.ascii else 'UNICODE'}\n"
            f"Color Mode: {'COLORED' if self.color else 'MONOCHROMATIC'}\n"
            f"Diff Mode: {'SIDE_BY_SIDE' if self.updown else 'UP_DOWN'}\n"
            f"Side-to-Side Min: {self.sideto_min}\n"
        )

class Settings:
    def __init__(self):
        self.reps: Dict[str, RepoSettings] = {}
        self.local = LocalSettings()
        self.reps["fup"] = RepoSettings().set_url("https://github.com/qxcodefup/arcade/blob/master/Readme.md")
        self.reps["ed"] = RepoSettings().set_url("https://github.com/qxcodeed/arcade/blob/master/Readme.md")
        self.reps["poo"] = RepoSettings().set_url("https://github.com/qxcodepoo/arcade/blob/master/Readme.md")

    def get_repo(self, course: str) -> RepoSettings:
        if course not in self.reps:
            raise ValueError(f"Course {course} not found in settings")
        return self.reps[course]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "reps": {k: v.to_dict() for k, v in self.reps.items()},
            "local": self.local.to_dict()
        }

    def from_dict(self, data: Dict[str, Any]):
        self.reps = {k: RepoSettings().from_dict(v) for k, v in data.get("reps", {}).items()}
        self.local = LocalSettings().from_dict(data.get("local", {}))
        return self
    
    def save_to_json(self, file: str):
        with open(file, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    def __str__(self):
        output = []
        output.append("Repositories:")
        maxlen = max([len(key) for key in self.reps])
        for key in self.reps:
            prefix = f"- {key.ljust(maxlen)}"
            if self.reps[key].file and self.reps[key].url:
                output.append(f"{prefix} : dual   : {self.reps[key].url} ; {self.reps[key].file}")
            elif self.reps[key].url:
                output.append(f"{prefix} : remote : {self.reps[key].url}")
            else:
                output.append(f"{prefix} : local  : {self.reps[key].file}")
        return "\n".join(output)


class SettingsParser:

    user_settings_file: Optional[str] = None

    def __init__(self):
        self.package_name = "tko"
        default_filename = "settings.json"
        if SettingsParser.user_settings_file is None:
            self.settings_file = os.path.abspath(default_filename) # backup for replit, dont remove
        else:
            self.settings_file = os.path.abspath(SettingsParser.user_settings_file)
        self.settings = self.load_settings()

    def load_settings(self) -> Settings:
        try:
            with open(self.settings_file, "r") as f:
                self.settings = Settings().from_dict(json.load(f))
                return self.settings
        except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
            return self.create_new_settings_file()

    def save_settings(self):
        self.settings.save_to_json(self.settings_file)

    def create_new_settings_file(self) -> Settings:
        self.settings = Settings()
        if not os.path.isdir(self.get_settings_dir()):
            os.makedirs(self.get_settings_dir(), exist_ok=True)
        self.save_settings()
        return self.settings

    def get_settings_dir(self) -> str:
        return os.path.dirname(self.settings_file)
    
    def get_language(self) -> str:
        return self.settings.local.lang




class Runner:
    def __init__(self):
        pass

    @staticmethod
    def subprocess_run(cmd: str, input_data: str="") -> Tuple[int, str, str]:
        answer = subprocess.run(cmd, shell=True, input=input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        err = ""
        if answer.returncode != 0:
            err = answer.stderr + Runner.decode_code(answer.returncode)

        # if running on windows
        if os.name == "nt":
            return answer.returncode, answer.stdout.encode("cp1252").decode("utf-8"), err
        return answer.returncode, answer.stdout, err

    @staticmethod
    def free_run(cmd: str) -> None:
        answer = subprocess.run(cmd, shell=True, text=True)
        if answer.returncode != 0 and answer.returncode != 1:
            print(Runner.decode_code(answer.returncode))


    @staticmethod
    def decode_code(returncode: int) -> str:
        code = 128 - returncode
        if code == 127:
            return ""
        if code == 139:
            return "fail: segmentation fault"
        if code == 134:
            return "fail: runtime exception"
        return "fail: execution error code " + str(code)

# class Runner:

#     def __init__(self):
#         pass

#     @staticmethod
#     def subprocess_run(cmd_list: List[str], input_data: str = "") -> Tuple[int, Any, Any]:
#         try:
#             p = subprocess.Popen(cmd_list, stdout=PIPE, stdin=PIPE, stderr=PIPE, universal_newlines=True)
#             stdout, stderr = p.communicate(input=input_data)
#             return p.returncode, stdout, stderr
#         except FileNotFoundError:
#             print("\n\nCommand not found: " + " ".join(cmd_list))
#             exit(1)




class Color:
    enabled = True
    map = {
        "red": "\u001b[31m",
        "r": "\u001b[31m",
        "green": "\u001b[32m",
        "g": "\u001b[32m",
        "yellow": "\u001b[33m",
        "y": "\u001b[33m",
        "blue": "\u001b[34m",
        "b": "\u001b[34m",
        "magenta": "\u001b[35m",
        "m": "\u001b[35m",
        "cyan": "\u001b[36m",
        "c": "\u001b[36m",
        "white": "\u001b[37m",
        "w": "\u001b[37m",
        "reset": "\u001b[0m",
        "bold": "\u001b[1m",
        "uline": "\u001b[4m",
    }

    @staticmethod
    def ljust(text: str, width: int) -> str:
        return text + " " * (width - Color.len(text))

    @staticmethod
    def center(text: str, width: int, filler: str) -> str:
        return (
            filler * ((width - Color.len(text)) // 2)
            + text
            + filler * ((width - Color.len(text) + 1) // 2)
        )

    @staticmethod
    def remove_colors(text: str) -> str:
        for color in Color.map.values():
            text = text.replace(color, "")
        return text

    @staticmethod
    def len(text):
        return len(Color.remove_colors(text))


def colour(color: str, text: str) -> str:
    return Color.map[color] + text + Color.map["reset"]


def colour_bold(color: str, text: str) -> str:
    return Color.map["bold"] + Color.map[color] + text + Color.map["reset"]


class __Symbols:
    def __init__(self):
        self.opening = ""
        self.neutral = ""
        self.success = ""
        self.failure = ""
        self.wrong = ""
        self.compilation = ""
        self.execution = ""
        self.unequal = ""
        self.equalbar = ""
        self.hbar = ""
        self.vbar = ""
        self.whitespace = ""  # interpunct
        self.newline = ""  # carriage return
        self.cfill = ""
        self.tab = ""
        self.arrow_up = ""

        self.ascii = False
        self.set_unicode()

    def get_mode(self) -> str:
        return "ASCII" if self.ascii else "UTF-8"

    def set_ascii(self):
        self.ascii = True

        self.opening = "=> "
        self.neutral = "."
        self.success = "S"
        self.failure = "X"
        self.wrong = "W"
        self.compilation = "C"
        self.execution = "E"
        self.unequal = "#"
        self.equalbar = "|"
        self.hbar = "─"
        self.vbar = "│"
        self.whitespace = "\u2E31"  # interpunct
        self.newline = "\u21B5"  # carriage return
        self.cfill = "_"
        self.tab = "    "
        self.arrow_up = "A"

    def set_unicode(self):
        self.ascii = False

        self.opening = "=> "
        self.neutral = "»"
        self.success = "✓"
        self.failure = "✗"
        self.wrong = "ω"
        self.compilation = "ϲ"
        self.execution = "ϵ"
        self.unequal = "├"
        self.equalbar = "│"
        self.hbar = "─"
        self.vbar = "│"
        self.whitespace = "\u2E31"  # interpunct
        self.newline = "\u21B5"  # carriage return
        self.cfill = "_"
        self.tab = "    "
        self.arrow_up = "↑"

    def set_colors(self):
        self.opening = colour("b", self.opening)
        self.neutral = colour("b", self.neutral)
        self.success = colour("g", self.success)
        self.failure = colour("r", self.failure)
        self.wrong = colour("r", self.wrong)
        self.compilation = colour("y", self.compilation)
        self.execution = colour("y", self.execution)
        self.unequal = colour("r", self.unequal)
        self.equalbar = colour("g", self.equalbar)


symbols = __Symbols()


class GSym:
    check = "✓"    # "✔"
    uncheck = "✗"  # "✘"

    opcheck = "ⴲⵔ"
    # opcheck = "✔▢"
    # opcheck = "🞕🞖" # erro Pedro
    # opcheck = "🟘🟗" # erro Pedro


    # oprightdown = "→↓"
    oprightdown = "➡️⬇️"    # azuzinho
    # oprightdown = "🠊🠋" # erro Pedro
    # oprightdown = "⮞⮟" # erro Pedro

    vcheck = opcheck[0]
    vuncheck = opcheck[1]
    right = "➡️"
    down = "⬇️"

    numbers = "0123456789***********"


def green(text):
    return colour("g", text)


def red(text):
    return colour("r", text)


def yellow(text):
    return colour("y", text)


def cyan(text):
    return colour("c", text)


class Report:
    __term_width: Optional[int] = None

    def __init__(self):
        pass

    @staticmethod
    def update_terminal_size():
        term_width = shutil.get_terminal_size().columns
        if term_width % 2 == 0:
            term_width -= 1
        Report.__term_width = term_width

    @staticmethod
    def get_terminal_size():
        if Report.__term_width is None:
            Report.update_terminal_size()

        return Report.__term_width

    @staticmethod
    def set_terminal_size(value: int):
        if value % 2 == 0:
            value -= 1
        Report.__term_width = value

    @staticmethod
    def centralize(
        text,
        sep=" ",
        left_border: Optional[str] = None,
        right_border: Optional[str] = None,
    ) -> str:
        if left_border is None:
            left_border = sep
        if right_border is None:
            right_border = sep
        term_width = Report.get_terminal_size()

        size = Color.len(text)
        pad = sep if size % 2 == 0 else ""
        tw = term_width - 2
        filler = sep * int(tw / 2 - size / 2)
        return left_border + pad + filler + text + filler + right_border



class ExecutionResult(Enum):
    UNTESTED          = "untested_"
    SUCCESS           = "correct__"
    WRONG_OUTPUT      = "wrong_out"
    COMPILATION_ERROR = "compilati"
    EXECUTION_ERROR   = "execution"

    @staticmethod
    def get_symbol(result) -> str:
        if result == ExecutionResult.UNTESTED:
            return symbols.neutral
        elif result == ExecutionResult.SUCCESS:
            return symbols.success
        elif result == ExecutionResult.WRONG_OUTPUT:
            return symbols.wrong
        elif result == ExecutionResult.COMPILATION_ERROR:
            return symbols.compilation
        elif result == ExecutionResult.EXECUTION_ERROR:
            return symbols.execution
        else:
            raise ValueError("Invalid result type")

    def __str__(self):
        return self.value

class CompilerError(Exception):
    pass


class DiffMode(Enum):
    FIRST = "MODE: SHOW FIRST FAILURE ONLY"
    ALL = "MODE: SHOW ALL FAILURES"
    QUIET = "MODE: SHOW NONE FAILURES"


class IdentifierType(Enum):
    OBI = "OBI"
    MD = "MD"
    TIO = "TIO"
    VPL = "VPL"
    SOLVER = "SOLVER"


class Identifier:
    def __init__(self):
        pass

    @staticmethod
    def get_type(target: str) -> IdentifierType:
        if os.path.isdir(target):
            return IdentifierType.OBI
        elif target.endswith(".md"):
            return IdentifierType.MD
        elif target.endswith(".tio"):
            return IdentifierType.TIO
        elif target.endswith(".vpl"):
            return IdentifierType.VPL
        else:
            return IdentifierType.SOLVER


class Unit:
    def __init__(self, case: str = "", inp: str = "", outp: str = "", grade: Optional[int] = None, source: str = ""):
        self.source = source  # stores the source file of the unit
        self.source_pad = 0  # stores the pad to justify the source file
        self.case = case  # name
        self.case_pad = 0  # stores the pad to justify the case name
        self.input = inp  # input
        self.output = outp  # expected output
        self.user: Optional[str] = None  # solver generated answer
        self.grade: Optional[int] = grade  # None represents proportional gr, 100 represents all
        self.grade_reduction: int = 0  # if grade is None, this atribute should be filled with the right grade reduction
        self.index = 0
        self.repeated: Optional[int] = None

        self.result: ExecutionResult = ExecutionResult.UNTESTED

    def __str__(self):
        index = str(self.index).zfill(2)
        grade = str(self.grade_reduction).zfill(3)
        rep = "" if self.repeated is None else "[" + str(self.repeated) + "]"
        return "(%s)[%s] GR:%s %s (%s) %s" % (ExecutionResult.get_symbol(self.result) + " " + self.result.value, index, grade, self.source.ljust(self.source_pad), self.case.ljust(self.case_pad), rep)


class Param:

    def __init__(self):
        pass

    class Basic:
        def __init__(self):
            self.index: Optional[int] = None
            self.label_pattern: Optional[str] = None
            self.is_up_down: bool = False
            self.diff_mode = DiffMode.FIRST
            self.filter: bool = False
            self.compact: bool = False

        def set_index(self, value: Optional[int]):
            self.index: Optional[int] = value
            return self

        def set_label_pattern(self, label_pattern: Optional[str]):
            self.label_pattern: Optional[str] = label_pattern
            return self
        
        def set_compact(self, value: bool):
            self.compact = value
            return self

        def set_up_down(self, value: bool):
            self.is_up_down = value
            return self
    
        def set_filter(self, value: bool):
            self.filter = value
            return self

        def set_diff_mode(self, value: DiffMode):
            self.diff_mode = value
            return self

    class Manip:
        def __init__(self):
            self.unlabel: bool = False
            self.to_sort: bool = False
            self.to_number: bool = False
        
        def set_unlabel(self, value: bool):
            self.unlabel = value
            return self
        
        def set_to_sort(self, value: bool):
            self.to_sort = value
            return self
        
        def set_to_number(self, value: bool):
            self.to_number = value
            return self




class Diff:

    @staticmethod
    def make_line_arrow_up(a: str, b: str) -> str:
        hdiff = ""
        first = True
        i = 0
        lim = max(len(a), len(b))
        while i < lim:
            if i >= len(a) or i >= len(b) or a[i] != b[i]:
                if first:
                    first = False
                    hdiff += symbols.arrow_up;
            else:
                hdiff += " "
            i += 1
        return hdiff

    @staticmethod
    def render_white(text: Optional[str], color: Optional[str] = None) -> Optional[str]:
        if text is None:
            return None
        if color is None:
            text = text.replace(' ', symbols.whitespace)
            text = text.replace('\n', symbols.newline + '\n')
            return text
        text = text.replace(' ', colour(color, symbols.whitespace))
        text = text.replace('\n', colour("r", symbols.newline) + '\n')
        return text

    # create a string with both ta and tb side by side with a vertical bar in the middle
    @staticmethod
    def side_by_side(ta: List[str], tb: List[str], unequal: str = symbols.unequal):
        cut = (Report.get_terminal_size() - 6) // 2
        upper = max(len(ta), len(tb))
        data = []

        for i in range(upper):
            a = ta[i] if i < len(ta) else "###############"
            b = tb[i] if i < len(tb) else "###############"
            if len(a) < cut:
                a = a.ljust(cut)
            # if len(a) > cut:
            #     a = a[:cut]
            if i >= len(ta) or i >= len(tb) or ta[i] != tb[i]:
                data.append(unequal + " " + a + " " + unequal + " " + b)
            else:
                data.append(symbols.vbar + " " + a + " " + symbols.vbar + " " + b)

        return "\n".join(data)

    # a_text -> clean full received
    # b_text -> clean full expected
    # first_failure -> index of the first line unmatched 
    @staticmethod
    def first_failure_diff(a_text: str, b_text: str, first_failure) -> str:
        def get(vet, index):
            if index < len(vet):
                return vet[index]
            return ""

        a_render = Diff.render_white(a_text).splitlines()
        b_render = Diff.render_white(b_text).splitlines()

        first_a = get(a_render, first_failure)
        first_b = get(b_render, first_failure)
        greater = max(Color.len(first_a), Color.len(first_b))
        lbefore = ""

        if first_failure > 0:
            lbefore = Color.remove_colors(get(a_render, first_failure - 1))
            greater = max(greater, Color.len(lbefore))

        out_a, out_b = Diff.colorize_2_lines_diff(first_a, first_b)

        postext  = symbols.vbar + " " + Color.ljust(out_a, greater) + colour("g", " (expected)") + "\n"
        postext += symbols.vbar + " " + Color.ljust(out_b, greater) + colour("r", " (received)") + "\n"
        postext += symbols.vbar + " " + Color.ljust(Diff.make_line_arrow_up(first_a, first_b), greater) + colour("b", " (mismatch)") + "\n"
        return postext

    @staticmethod
    def find_first_mismatch(line_a: str, line_b: str) -> int: 
        i = 0
        while i < len(line_a) and i < len(line_b):
            if line_a[i] != line_b[i]:
                return i
            i += 1
        return i
    
    @staticmethod
    def colorize_2_lines_diff(line_a: str, line_b: str, neutral:str="w", expected:str="g", received:str="r") -> Tuple[str, str]:
        pos = Diff.find_first_mismatch(line_a, line_b)
        a_out = colour(neutral, line_a[0:pos]) + colour(expected, line_a[pos:])
        b_out = colour(neutral, line_b[0:pos]) + colour(received, line_b[pos:])
        return (a_out, b_out)
    
    

    # return a tuple of two strings with the diff and the index of the  first mismatch line
    @staticmethod
    def render_diff(a_text: str, b_text: str, pad: Optional[bool] = None) -> Tuple[List[str], List[str], int]:
        a_lines = a_text.splitlines()
        b_lines = b_text.splitlines()

        a_output = []
        b_output = []

        a_size = len(a_lines)
        b_size = len(b_lines)
        
        first_failure = -1

        cut: int = 0
        if pad is True:
            cut = (Report.get_terminal_size() - 6)// 2

        max_size = max(a_size, b_size)

        # lambda function to return element in index i or empty if out of bounds
        def get(vet, index):
            out = ""
            if index < len(vet):
                out = vet[index]
            if pad is None:
                return out
            return out[:cut].ljust(cut)

        # get = lambda vet, i: vet[i] if i < len(vet) else ""

        for i in range(max_size):
            a_data = get(a_lines, i)
            b_data = get(b_lines, i)
            
            if i >= a_size or i >= b_size or a_lines[i] != b_lines[i]:
                if first_failure == -1:
                    first_failure = i
                a_out, b_out = Diff.colorize_2_lines_diff(a_data, b_data, "yellow")
                a_output.append(a_out)
                b_output.append(b_out)
            else:
                a_output.append(a_data)
                b_output.append(b_data)

        return a_output, b_output, first_failure

    @staticmethod
    def mount_up_down_diff(unit: Unit) -> str:
        output = io.StringIO()

        string_input = unit.input
        string_expected = unit.output
        string_received = unit.user

        dotted = "-"

        expected_lines, received_lines, first_failure = Diff.render_diff(string_expected, string_received)
        string_input = "\n".join([symbols.vbar + " " + line for line in string_input.split("\n")])[0:-2]
        unequal = symbols.unequal
        if unit.result == ExecutionResult.EXECUTION_ERROR:
            unequal = symbols.vbar
        expected_lines, received_lines = Diff.put_left_equal(expected_lines, received_lines, unequal)

        output.write(Report.centralize("", symbols.hbar, "╭") + "\n")
        output.write(Report.centralize(str(unit), " ", symbols.vbar) + "\n")
        output.write(Report.centralize(colour("b", " INPUT "), symbols.hbar, "├") + "\n")
        output.write(string_input)
        output.write(Report.centralize(colour("g", " EXPECTED "), symbols.hbar, "├") + "\n")
        output.write("\n".join(expected_lines) + "\n")
        output.write(Report.centralize(colour("r", " RECEIVED "), symbols.hbar, "├") + "\n")
        output.write("\n".join(received_lines) + "\n")
        if unit.result != ExecutionResult.EXECUTION_ERROR:
            output.write(Report.centralize(colour("bold", " WHITESPACE "),  symbols.hbar, "├") + "\n")
            output.write(Diff.first_failure_diff(string_expected, string_received, first_failure))
        output.write(Report.centralize("",  symbols.hbar, "╰") + "\n")

        return output.getvalue()

    @staticmethod
    def put_left_equal(exp_lines: str, rec_lines: str, unequal:str=symbols.unequal):

        max_size = max(len(exp_lines), len(rec_lines))

        for i in range(max_size):
            if i >= len(exp_lines) or i >= len(rec_lines) or (exp_lines[i] != rec_lines[i]):
                exp_lines[i] = unequal + " " + exp_lines[i]
                rec_lines[i] = unequal + " " + rec_lines[i]
            else:
                exp_lines[i] = symbols.vbar + " " + exp_lines[i]
                rec_lines[i] = symbols.vbar + " " + rec_lines[i]
        
        return exp_lines, rec_lines
            

    @staticmethod
    def mount_side_by_side_diff(unit: Unit) -> str:

        def title_side_by_side(left, right, filler=" ", middle=" ", prefix=""):
            half = int((Report.get_terminal_size() - len(middle)) / 2)
            line = ""
            a = Color.center(left, half, filler)
            if Color.len(a) > half:
                a = a[:half]
            line += a
            line += middle
            b = Color.center(right, half, filler)
            if Color.len(b) > half:
                b = b[:half]
            line += b
            if prefix != "":
                line = prefix + line[1:]
            return line

        output = io.StringIO()

        string_input = unit.input
        string_expected = unit.output
        string_received = unit.user

        dotted = "-"
        vertical_separator = symbols.vbar
        hbar = symbols.hbar

        expected_lines, received_lines, first_failure = Diff.render_diff(string_expected, string_received, True)
        output.write(Report.centralize("", hbar, "╭") + "\n")
        output.write(Report.centralize(str(unit), " ", "│") + "\n")
        input_header = colour("b", " INPUT ")
        output.write(title_side_by_side(input_header, input_header, hbar, "┬", "├") + "\n")
        if (string_input != ""):
            output.write(Diff.side_by_side(string_input.split("\n")[:-1], string_input.split("\n")[:-1]) + "\n")
        expected_header = colour("g", " EXPECTED ")
        received_header = colour("r", " RECEIVED ")
        output.write(title_side_by_side(expected_header, received_header, hbar, "┼", "├") + "\n")
        unequal = symbols.unequal
        if unit.result == ExecutionResult.EXECUTION_ERROR:
            unequal = symbols.vbar
        output.write(Diff.side_by_side(expected_lines, received_lines, unequal) + "\n")
        if unit.result != ExecutionResult.EXECUTION_ERROR:
            output.write(Report.centralize(colour("bold", " WHITESPACE "),  symbols.hbar, "├") + "\n")
            output.write(Diff.first_failure_diff(string_expected, string_received, first_failure))
        output.write(Report.centralize("",  symbols.hbar, "╰") + "\n")

        return output.getvalue()




class Down:

    ts_draft = (r'let _cin_ : string[] = [];' + '\n'
                r'try { _cin_ = require("fs").readFileSync(0).toString().split(/\r?\n/); } catch(e){}' + '\n'
                r'let input = () : string => _cin_.length === 0 ? "" : _cin_.shift()!;' + '\n'
                r'let write = (text: any, end:string="\n")=> process.stdout.write("" + text + end);' + '\n')

    js_draft = (r'let __lines = require("fs").readFileSync(0).toString().split("\n");'  + '\n'
                r'let input = () => __lines.length === 0 ? "" : __lines.shift();' + '\n'
                r'let write = (text, end="\n") => process.stdout.write("" + text + end);') + '\n'
    
    c_draft = '#include <stdio.h>\n\nint main() {\n    return 0;\n}\n\n'
    cpp_draft = '#include <iostream>\n\nint main() {\n}\n\n'

    drafts = {'c': c_draft, 'cpp': cpp_draft, 'ts': ts_draft, 'js': js_draft}
    # def __init__(self):
    #     self.drafts = {}
    #     self.drafts['c'] = Down.c_draft
    #     self.drafts['cpp'] = Down.cpp_draft
    #     self.drafts['ts'] = Down.ts_draft
    #     self.drafts['js'] = Down.js_draft

    # @staticmethod
    # def update():
    #     if os.path.isfile(".info"):
    #         data = open(".info", "r").read().split("\n")[0]
    #         data = data.split(" ")
    #         discp = data[0]
    #         label = data[1]
    #         ext = data[2]
    #         Down.entry_unpack(".", discp, label, ext)
    #     else:
    #         print("No .info file found, skipping update...")

    @staticmethod
    def __create_file(content, path, label=""):
        with open(path, "w") as f:
            f.write(content)
        print(path, label)

    @staticmethod
    def __unpack_json(loaded, destiny, lang: str):
        # extracting all files to folder
        for entry in loaded["upload"]:
            if entry["name"] == "vpl_evaluate.cases":
                Down.__compare_and_save(entry["contents"], os.path.join(destiny, "cases.tio"))

        # for entry in loaded["keep"]:
        #    Down.compare_and_save(entry["contents"], os.path.join(destiny, entry["name"]))

        # for entry in loaded["required"]:
        #    path = os.path.join(destiny, entry["name"])
        #    Down.compare_and_save(entry["contents"], path)

        if "draft" in loaded:
            if lang in loaded["draft"]:
                for file in loaded["draft"][lang]:
                    path = os.path.join(destiny, file["name"])
                    Down.__create_file(file["contents"], path, "(Draft)")

    @staticmethod
    def __compare_and_save(content, path):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.encode("utf-8").decode("utf-8"))
            print(path + " (New)")
        else:
            if open(path).read() != content:
                print(path + " (Updated)")
                with open(path, "w") as f:
                    f.write(content)
            else:
                print(path + " (Unchanged)")
    
    @staticmethod
    def __down_problem_def(destiny, cache_url) -> Tuple[str, str]:
        # downloading Readme
        readme = os.path.join(destiny, "Readme.md")
        [tempfile, __content] = urllib.request.urlretrieve(cache_url + "Readme.md")
        content = ""
        try:
            content = open(tempfile, encoding="utf-8").read()
        except:
            content = open(tempfile).read()

        Down.__compare_and_save(content, readme)
        
        # downloading mapi
        mapi = os.path.join(destiny, "mapi.json")
        urllib.request.urlretrieve(cache_url + "mapi.json", mapi)
        return readme, mapi

    @staticmethod
    def __create_problem_folder(_course, activity):
        # create dir
        destiny = activity
        if not os.path.exists(destiny):
            os.makedirs(destiny, exist_ok=True)
        else:
            print("problem folder", destiny, "found, merging content.")

        return destiny


    @staticmethod
    def download_problem(course: str, activity: str, language: Optional[str]) -> bool:
        sp = SettingsParser()
        settings = sp.load_settings()
        rep = settings.get_repo(course)
        # if rep.url == "":
        #     print("fail: course", course, "is not a remote course")
        #     return False
        file = rep.get_file()
        item = Game(file).get_task(activity)
        if not item.link.startswith("http"):
            print("fail: link for activity is not a remote link")
            return
        cfg = RemoteCfg(item.link)
        cache_url = os.path.dirname(cfg.get_raw_url()) + "/.cache/"
    
        # rep = reps[course]
        # cfg = RemoteCfg()
        # cfg.from_url(rep.url)
        # url = cfg.get_raw_url()
        # basedir = os.path.dirname(url) + "/base/" 
        # index_url = basedir + activity + "/"
        # cache_url = index_url + ".cache/"

        # downloading Readme
        try:
            destiny = Down.__create_problem_folder(course, activity)
            #print("debug", cache_url)
            [_readme_path, mapi_path] = Down.__down_problem_def(destiny, cache_url)
        except urllib.error.HTTPError:
            print("fail: activity not found in course url")
            # verifi if destiny folder is empty and remove it
            if len(os.listdir(destiny)) == 0:
                os.rmdir(destiny)
            return False

        with open(mapi_path) as f:
            loaded_json = json.load(f)
        os.remove(mapi_path)

        language_def = SettingsParser().get_language()
        ask_ext = False
        if language is None:
            if language_def != "ask":
                language = language_def
            else:
                print("Choose extension for draft: [c, cpp, py, ts, js, java]: ", end="")
                language = input()
                ask_ext = True
        
        Down.__unpack_json(loaded_json, destiny, language)
        Down.__download_drafts(loaded_json, destiny, language, cache_url, ask_ext)
        return True

    @staticmethod
    def __download_drafts(loaded_json, destiny, language, cache_url, ask_ext):
        if len(loaded_json["required"]) == 1:  # you already have the students file
            return

        if "draft" in loaded_json and language in loaded_json["draft"]:
            pass
        else:
            try:
                draft_path = os.path.join(destiny, "draft." + language)
                urllib.request.urlretrieve(cache_url + "draft." + language, draft_path)
                print(draft_path + " (Draft) Rename before modify.")

            except urllib.error.HTTPError:  # draft not found
                filename = "draft."
                draft_path = os.path.join(destiny, filename + language)
                if not os.path.exists(draft_path):
                    with open(draft_path, "w") as f:
                        if language in Down.drafts:
                            f.write(Down.drafts[language])
                        else:
                            f.write("")
                    print(draft_path, "(Empty)")
        
        if ask_ext:
            print("\nYou can choose default extension with command\n$ tko config -l <extension>")




def check_tool(name):
    if which(name) is None:
        raise CompilerError("fail: " + name + " executable not found")


class Solver:
    def __init__(self, solver_list: List[str]):
        self.path_list: List[str] = [Solver.__add_dot_bar(path) for path in solver_list]
        
        self.temp_dir = tempfile.mkdtemp()
        self.error_msg: str = ""
        self.executable: str = ""
        if len(self.path_list) > 0:
            self.prepare_exec()

    def prepare_exec(self) -> None:
        path = self.path_list[0]

        if path.endswith(".py"):
            self.executable = "python " + path
        elif path.endswith(".js"):
            self.__prepare_js()
        elif path.endswith(".ts"):
            self.__prepare_ts()
        elif path.endswith(".java"):
            self.__prepare_java()
        elif path.endswith(".c"):
            self.__prepare_c()
        elif path.endswith(".cpp"):
            self.__prepare_cpp()
        elif path.endswith(".sql"):
            self.__prepare_sql()
        else:
            self.executable = path

    def __prepare_java(self):
        check_tool("javac")

        solver = self.path_list[0]

        filename = os.path.basename(solver)
        # tempdir = os.path.dirname(self.path_list[0])

        cmd = ["javac"] + self.path_list + ['-d', self.temp_dir]
        cmd = " ".join(cmd)
        return_code, stdout, stderr = Runner.subprocess_run(cmd)
        print(stdout)
        print(stderr)
        if return_code != 0:
            raise CompilerError(stdout + stderr)
        self.executable = "java -cp " + self.temp_dir + " " + filename[:-5]  # removing the .java

    def __prepare_js(self):
        check_tool("node")
        solver = self.path_list[0]
        self.executable = "node " + solver

    def __prepare_sql(self):
        check_tool("sqlite3")
        self.executable = "cat " + " ".join(self.path_list) + " | sqlite3"

    def __prepare_ts(self):
        transpiler = "esbuild"
        if os.name == "nt":
            transpiler += ".cmd"

        check_tool(transpiler)
        check_tool("node")

        solver = self.path_list[0]

        filename = os.path.basename(solver)
        source_list = self.path_list
        cmd = [transpiler] + source_list + ["--outdir=" + self.temp_dir, "--format=cjs", "--log-level=error"]
        return_code, stdout, stderr = Runner.subprocess_run(" ".join(cmd))
        print(stdout + stderr)
        if return_code != 0:
            raise CompilerError(stdout + stderr)
        jsfile = os.path.join(self.temp_dir, filename[:-3] + ".js")
        self.executable = "node " + jsfile  # renaming solver to main
    
    def __prepare_c_cpp(self, pre_args: List[str], pos_args: List[str]):
        # solver = self.path_list[0]
        tempdir = self.temp_dir
        source_list = self.path_list
        # print("Using the following source files: " + str([os.path.basename(x) for x in source_list]))
        
        exec_path = os.path.join(tempdir, ".a.out")
        cmd = pre_args + source_list + ["-o", exec_path] + pos_args
        return_code, stdout, stderr = Runner.subprocess_run(" ".join(cmd))
        if return_code != 0:
            raise CompilerError(stdout + stderr)
        self.executable = exec_path

    def __prepare_c(self):
        check_tool("gcc")
        pre = ["gcc", "-Wall"]
        pos = ["-lm", "-lutil"]
        self.__prepare_c_cpp(pre, pos)

    def __prepare_cpp(self):
        check_tool("g++")
        pre = ["g++", "-std=c++17", "-Wall", "-Wextra", "-Werror"]
        pos = []
        self.__prepare_c_cpp(pre, pos)

    @staticmethod
    def __add_dot_bar(solver: str) -> str:
        if os.sep not in solver and os.path.isfile("." + os.sep + solver):
            solver = "." + os.sep + solver
        return solver
    


class FileSource:
    def __init__(self, label, input_file, output_file):
        self.label = label
        self.input_file = input_file
        self.output_file = output_file

    def __eq__(self, other):
        return self.label == other.label and self.input_file == other.input_file and \
                self.output_file == other.output_file


class PatternLoader:
    pattern: str = ""

    def __init__(self):
        parts = PatternLoader.pattern.split(" ")
        self.input_pattern = parts[0]
        self.output_pattern = parts[1] if len(parts) > 1 else ""
        self._check_pattern()

    def _check_pattern(self):
        self.__check_double_wildcard()
        self.__check_missing_wildcard()

    def __check_double_wildcard(self):
        if self.input_pattern.count("@") > 1 or self.output_pattern.count("@") > 1:
            raise ValueError("  fail: the wildcard @ should be used only once per pattern")

    def __check_missing_wildcard(self):
        if "@" in self.input_pattern and "@" not in self.output_pattern:
            raise ValueError("  fail: is input_pattern has the wildcard @, the input_patter should have too")
        if "@" not in self.input_pattern and "@" in self.output_pattern:
            raise ValueError("  fail: is output_pattern has the wildcard @, the input_pattern should have too")

    def make_file_source(self, label):
        return FileSource(label, self.input_pattern.replace("@", label), self.output_pattern.replace("@", label))

    def get_file_sources(self, filename_list: List[str]) -> List[FileSource]:
        input_re = self.input_pattern.replace(".", "\\.")
        input_re = input_re.replace("@", "(.*)")
        file_source_list = []
        for filename in filename_list:
            match = re.findall(input_re, filename)
            if not match:
                continue
            label = match[0]
            file_source = self.make_file_source(label)
            if file_source.output_file not in filename_list:
                print("fail: file " + file_source.output_file + " not found")
            else:
                file_source_list.append(file_source)
        return file_source_list

    def get_odd_files(self, filename_list) -> List[str]:
        matched = []
        sources = self.get_file_sources(filename_list)
        for source in sources:
            matched.append(source.input_file)
            matched.append(source.output_file)
        unmatched = [file for file in filename_list if file not in matched]
        return unmatched




class VplParser:
    @staticmethod
    def finish(text):
        return text if text.endswith("\n") else text + "\n"

    @staticmethod
    def unwrap(text):
        while text.endswith("\n"):
            text = text[:-1]
        if text.startswith("\"") and text.endswith("\""):
            text = text[1:-1]
        return VplParser.finish(text)

    @staticmethod
    class CaseData:
        def __init__(self, case="", inp="", outp="", grade: Optional[int] = None):
            self.case: str = case
            self.input: str = VplParser.finish(inp)
            self.output: str = VplParser.unwrap(VplParser.finish(outp))
            self.grade: Optional[int] = grade

        def __str__(self):
            return "case=" + self.case + '\n' \
                   + "input=" + self.input \
                   + "output=" + self.output \
                   + "gr=" + str(self.grade)

    regex_vpl_basic = r"case= *([ \S]*) *\n *input *=(.*?)^ *output *=(.*)"
    regex_vpl_extended = r"case= *([ \S]*) *\n *input *=(.*?)^ *output *=(.*?)^ *grade *reduction *= *(\S*)% *\n?"

    @staticmethod
    def filter_quotes(x):
        return x[1:-2] if x.startswith('"') else x

    @staticmethod
    def split_cases(text: str) -> List[str]:
        regex = r"^ *[Cc]ase *="
        subst = "case="
        text = re.sub(regex, subst, text, 0, re.MULTILINE | re.DOTALL)
        return ["case=" + t for t in text.split("case=")][1:]

    @staticmethod
    def extract_extended(text) -> Optional[CaseData]:
        f = re.match(VplParser.regex_vpl_extended, text, re.MULTILINE | re.DOTALL)
        if f is None:
            return None
        try:
            gr = int(f.group(4))
        except ValueError:
            gr = None
        return VplParser.CaseData(f.group(1), f.group(2), f.group(3), gr)

    @staticmethod
    def extract_basic(text) -> Optional[CaseData]:
        m = re.match(VplParser.regex_vpl_basic, text, re.MULTILINE | re.DOTALL)
        if m is None:
            return None
        return VplParser.CaseData(m.group(1), m.group(2), m.group(3), None)

    @staticmethod
    def parse_vpl(content: str) -> List[CaseData]:
        text_cases = VplParser.split_cases(content)
        seq: List[VplParser.CaseData] = []

        for text in text_cases:
            case = VplParser.extract_extended(text)
            if case is not None:
                seq.append(case)
                continue
            case = VplParser.extract_basic(text)
            if case is not None:
                seq.append(case)
                continue
            print("invalid case: " + text)
            exit(1)
        return seq

    @staticmethod
    def to_vpl(unit: CaseData):
        text = "case=" + unit.case + "\n"
        text += "input=" + unit.input
        text += "output=\"" + unit.output + "\"\n"
        if unit.grade is not None:
            text += "grade reduction=" + str(unit.grade) + "%\n"
        return text


class Loader:
    regex_tio = r"^ *>>>>>>>> *(.*?)\n(.*?)^ *======== *\n(.*?)^ *<<<<<<<< *\n?"

    def __init__(self):
        pass

    @staticmethod
    def parse_cio(text, source, crude_mode=False):
        unit_list = []
        text = "\n" + text

        pattern = r'```.*?\n(.*?)```' # get only inside code blocks
        code = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
        # join all code blocks found
        text = "\n" + "\n".join(code)

        pieces: List[Dict[str, List[str], List[str]]] = [] # header, input, output

        open_case = False
        for line in text.split("\n"):
            if line.startswith("#__case") or line.startswith("#TEST_CASE"):
                pieces.append({"header": line, "input": [], "output": []})
                open_case = True
            elif open_case:
                pieces[-1]["output"].append(line)
                if line.startswith("$end"):
                    open_case = False

        # concatenando testes contínuos e finalizando testes sem $end
        for i in range(len(pieces)):
            output = pieces[i]["output"]
            if output[-1] != "$end" and i < len(pieces) - 1:
                pieces[i + 1]["output"] = output + pieces[i + 1]["output"]
                output.append("$end")

        # removendo linhas vazias e criando input das linhas com $
        for piece in pieces:
            piece["input"]  = [line[1:] for line in piece["output"] if line.startswith("$")]
            piece["output"] = [line for line in piece["output"] if line != "" and not line.startswith("#")]

        for piece in pieces:
            case = " ".join(piece["header"].split(" ")[1:])
            input = "\n".join(piece["input"]) + "\n"
            output = "\n".join(piece["output"]) + "\n"
            unit_list.append(Unit(case, input, output, None, source))

        for unit in unit_list:
            unit.fromCio = True

        return unit_list

    @staticmethod
    def parse_tio(text: str, source: str = "") -> List[Unit]:

        # identifica se tem grade e retorna case name e grade
        def parse_case_grade(value: str) -> Tuple[str, Optional[int]]:
            if value.endswith("%"):
                words = value.split(" ")
                last = value.split(" ")[-1]
                _case = " ".join(words[:-1])
                grade_str = last[:-1]           # ultima palavra sem %
                try:
                    _grade = int(grade_str)
                    return _case, _grade
                except ValueError:
                    pass
            return value, None

        matches = re.findall(Loader.regex_tio, text, re.MULTILINE | re.DOTALL)
        unit_list = []
        for m in matches:
            case, grade = parse_case_grade(m[0])
            unit_list.append(Unit(case, m[1], m[2], grade, source))
        return unit_list

    @staticmethod
    def parse_vpl(text: str, source: str = "") -> List[Unit]:
        data_list = VplParser.parse_vpl(text)
        output: List[Unit] = []
        for m in data_list:
            output.append(Unit(m.case, m.input, m.output, m.grade, source))
        return output

    @staticmethod
    def parse_dir(folder) -> List[Unit]:
        pattern_loader = PatternLoader()
        files = sorted(os.listdir(folder))
        matches = pattern_loader.get_file_sources(files)

        unit_list: List[Unit] = []
        try:
            for m in matches:
                unit = Unit()
                unit.source = os.path.join(folder, m.label)
                unit.grade = 100
                with open(os.path.join(folder, m.input_file)) as f:
                    value = f.read()
                    unit.input = value + ("" if value.endswith("\n") else "\n")
                with open(os.path.join(folder, m.output_file)) as f:
                    value = f.read()
                    unit.output = value + ("" if value.endswith("\n") else "\n")
                unit_list.append(unit)
        except FileNotFoundError as e:
            print(str(e))
        return unit_list

    @staticmethod
    def parse_source(source: str) -> List[Unit]:
        if os.path.isdir(source):
            return Loader.parse_dir(source)
        if os.path.isfile(source):
            #  if PreScript.exists():
            #      source = PreScript.process_source(source)
            with open(source) as f:
                content = f.read()
            if source.endswith(".vpl"):
                return Loader.parse_vpl(content, source)
            elif source.endswith(".tio"):
                return Loader.parse_tio(content, source)
            elif source.endswith(".md"):
                tests = Loader.parse_tio(content, source)
                tests += Loader.parse_cio(content, source)
                return tests
            else:
                print("warning: target format do not supported: " + source)  # make this a raise
        else:
            raise FileNotFoundError('warning: unable to find: ' + source)
        return []




class Writer:

    def __init__(self):
        pass

    @staticmethod
    def to_vpl(unit: Unit):
        text = "case=" + unit.case + "\n"
        text += "input=" + unit.input
        text += "output=\"" + unit.output + "\"\n"
        if unit.grade is None:
            text += "\n"
        else:
            text += "grade reduction=" + str(unit.grade).zfill(3) + "%\n"
        return text

    @staticmethod
    def to_tio(unit: Unit):
        text = ">>>>>>>>"
        if unit.case != '':
            text += " " + unit.case
        if unit.grade is not None:
            text += " " + str(unit.grade) + "%"
        text += '\n' + unit.input
        text += "========\n"
        text += unit.output
        if unit.output != '' and unit.output[-1] != '\n':
            text += '\n'
        text += "<<<<<<<<\n"
        return text

    @staticmethod
    def save_dir_files(folder: str, pattern_loader: PatternLoader, label: str, unit: Unit) -> None:
        file_source = pattern_loader.make_file_source(label)
        with open(os.path.join(folder, file_source.input_file), "w") as f:
            f.write(unit.input)
        with open(os.path.join(folder, file_source.output_file), "w") as f:
            f.write(unit.output)

    @staticmethod
    def save_target(target: str, unit_list: List[Unit], force: bool = False):
        def ask_overwrite(file):
            print("file " + file + " found. Overwrite? (y/n):")
            resp = input()
            if resp.lower() == 'y':
                print("overwrite allowed")
                return True
            print("overwrite denied\n")
            return False

        def save_dir(_target: str, _unit_list):
            folder = _target
            pattern_loader = PatternLoader()
            number = 0
            for unit in _unit_list:
                Writer.save_dir_files(folder, pattern_loader, str(number).zfill(2), unit)
                number += 1

        def save_file(_target, _unit_list):
            if _target.endswith(".tio"):
                _new = "\n".join([Writer.to_tio(unit) for unit in _unit_list])
            else:
                _new = "\n".join([Writer.to_vpl(unit) for unit in _unit_list])

            file_exists = os.path.isfile(_target)

            if file_exists:
                _old = open(_target).read()
                if _old == _new:
                    print("no changes in test file")
                    return

            if not file_exists or (file_exists and (force or ask_overwrite(_target))):
                with open(_target, "w") as f:
                    f.write(_new)

                    if not force:
                        print("file " + _target + " wrote")

        target_type = Identifier.get_type(target)
        if target_type == IdentifierType.OBI:
            save_dir(target, unit_list)
        elif target_type == IdentifierType.TIO or target_type == IdentifierType.VPL:
            save_file(target, unit_list)
        else:
            print("fail: target " + target + " do not supported for build operation\n")



# generate label for cases


class LabelFactory:
    def __init__(self):
        self._label = ""
        self._index = -1

    def index(self, value: int):
        try:
            self._index = int(value)
        except ValueError:
            raise ValueError("Index on label must be a integer")
        return self

    def label(self, value: str):
        self._label = value
        return self

    def generate(self):
        label = LabelFactory.trim_spaces(self._label)
        label = LabelFactory.remove_old_index(label)
        if self._index != -1:
            index = str(self._index).zfill(2)
            if label != "":
                return index + " " + label
            else:
                return index
        return label

    @staticmethod
    def trim_spaces(text):
        parts = text.split(" ")
        parts = [word for word in parts if word != '']
        return " ".join(parts)

    @staticmethod
    def remove_old_index(label):
        split_label = label.split(" ")
        if len(split_label) > 0:
            try:
                int(split_label[0])
                return " ".join(split_label[1:])
            except ValueError:
                return label


class Wdir:
    def __init__(self):
        self.solver: Optional[Solver] = None
        self.source_list: List[str] = []
        self.pack_list: List[List[Unit]] = []
        self.unit_list: List[Unit] = []

    def set_solver(self, solver_list: List[str]):
        if len(solver_list) > 0:
            self.solver = Solver(solver_list)
        return self

    def set_sources(self, source_list: List[str]):
        self.source_list = source_list
        return self

    def set_target_list(self, target_list: List[str]):
        target_list = [t for t in target_list if t != ""]
        for target in target_list:
            if not os.path.exists(target):
                raise FileNotFoundError(colour("red", "fail: ") + target + " not found")

        solvers = [target for target in target_list if Identifier.get_type(target) == IdentifierType.SOLVER]
        sources = [target for target in target_list if Identifier.get_type(target) != IdentifierType.SOLVER]
        
        self.set_solver(solvers)
        self.set_sources(sources)
        return self

    def set_cmd(self, exec_cmd: Optional[str]):
        if exec_cmd is None:
            return self
        if self.solver is not None:
            print("fail: if using --cmd, don't pass source files to target")
        self.solver = Solver([])
        self.solver.executable = exec_cmd
        return self

    def build(self):
        loading_failures = 0
        for source in self.source_list:
            try:
                self.pack_list.append(Loader.parse_source(source))
            except FileNotFoundError as e:
                print(str(e))
                loading_failures += 1
                pass
        if loading_failures > 0 and loading_failures == len(self.source_list):
            raise FileNotFoundError("failure: none source found")
        self.unit_list = sum(self.pack_list, [])
        self.__number_and_mark_duplicated()
        self.__calculate_grade()
        self.__pad()
        return self

    def calc_grade(self) -> int:
        grade = 100
        for case in self.unit_list:
            if not case.repeated and (case.user is None or case.output != case.user):
                grade -= case.grade_reduction
        return max(0, grade)

    # put all the labels with the same length
    def __pad(self):
        if len(self.unit_list) == 0:
            return
        max_case = max([len(x.case) for x in self.unit_list])
        max_source = max([len(x.source) for x in self.unit_list])
        for unit in self.unit_list:
            unit.case_pad = max_case
            unit.source_pad = max_source

    # select a single unit to execute exclusively
    def filter(self, param: Param.Basic):
        index = param.index
        if index is not None:
            if 0 <= index < len(self.unit_list):
                self.unit_list = [self.unit_list[index]]
            else:
                raise ValueError("Index Number out of bounds: " + str(index))
        return self

    # calculate the grade reduction for the cases without grade
    # the grade is proportional to the number of unique cases
    def __calculate_grade(self):
        unique_count = len([x for x in self.unit_list if not x.repeated])
        for unit in self.unit_list:
            if unit.grade is None:
                unit.grade_reduction = math.floor(100 / unique_count)
            else:
                unit.grade_reduction = unit.grade

    # number the cases and mark the repeated
    def __number_and_mark_duplicated(self):
        new_list = []
        index = 0
        for unit in self.unit_list:
            unit.index = index
            index += 1
            search = [x for x in new_list if x.input == unit.input]
            if len(search) > 0:
                unit.repeated = search[0].index
            new_list.append(unit)
        self.unit_list = new_list

    # sort, unlabel ou rename using the param received
    def manipulate(self, param: Param.Manip):
        # filtering marked repeated
        self.unit_list = [unit for unit in self.unit_list if unit.repeated is None]
        if param.to_sort:
            self.unit_list.sort(key=lambda v: len(v.input))
        if param.unlabel:
            for unit in self.unit_list:
                unit.case = ""
        if param.to_number:
            number = 00
            for unit in self.unit_list:
                unit.case = LabelFactory().label(unit.case).index(number).generate()
                number += 1

    def unit_list_resume(self):
        return "\n".join([str(unit) for unit in self.unit_list])

    def resume(self) -> str:

        def sources() -> str:
            out = []
            if len(self.pack_list) == 0:
                out.append(symbols.failure)
            for i in range(len(self.pack_list)):
                nome: str = self.source_list[i].split(os.sep)[-1]
                out.append(nome + "(" + str(len(self.pack_list[i])).zfill(2) + ")")
            return colour("green", "base:") + "[" + ", ".join(out) + "]"

        def solvers() -> str:
            path_list = [] if self.solver is None else self.solver.path_list
            out = ""
            if self.solver is not None and len(path_list) == 0: # free_cmd
                out = "free cmd"
            else:
                out = ", ".join([os.path.basename(path) for path in path_list])
            return colour("green", "prog:") + "[" + out + "]"

        # folder = os.getcwd().split(os.sep)[-1]
        #tests_count = (colour("tests:", Color.GREEN) +
        #               str(len([x for x in self.unit_list if x.repeated is None])).zfill(2))

        return symbols.opening + sources() + " " + solvers()




class Execution:

    def __init__(self):
        pass

    # run a unit using a solver and return if the result is correct
    @staticmethod
    def run_unit(solver: Solver, unit: Unit) -> ExecutionResult:
        cmd = solver.executable
        return_code, stdout, stderr = Runner.subprocess_run(cmd, unit.input)
        unit.user = stdout + stderr
        if return_code != 0:
            return ExecutionResult.EXECUTION_ERROR
        if unit.user == unit.output:
            return ExecutionResult.SUCCESS
        return ExecutionResult.WRONG_OUTPUT


class FilterMode:

    @staticmethod
    def deep_copy_and_change_dir():
        # path to ~/.tko_filter
        filter_path = os.path.join(os.path.expanduser("~"), ".tko_filter")

        # verify if filter command is available
        if shutil.which("filter") is None:
            print("ERROR: filter command not found")
            print("Install feno with 'pip install feno'")
            exit(1)

        subprocess.run(["filter", "-rf", ".", "-o", filter_path])

        os.chdir(filter_path)


class Run:

    def __init__(self, target_list: List[str], exec_cmd: Optional[str], param: Param.Basic):
        self.target_list = target_list
        self.exec_cmd = exec_cmd
        self.param = param
        self.wdir = None

    def execute(self):
        self.remove_duplicates()
        self.change_targets_to_filter_mode()
        if not self.build_wdir():
            return
        if self.missing_target():
            return
        if self.list_mode():
            return
        if self.free_run():
            return
        self.diff_mode()
        return

    def remove_duplicates(self):
        # remove duplicates in target list keeping the order
        self.target_list = list(dict.fromkeys(self.target_list))

    def change_targets_to_filter_mode(self):
        # modo de filtragem, antes de processar os dados, copiar tudo para o diretório temp fixo
        # filtrar os solvers para então continuar com a execução
        if self.param.filter:
            old_dir = os.getcwd()

            print(Report.centralize(" Entering in filter mode ", "═"))
            FilterMode.deep_copy_and_change_dir()  
            # search for target outside . dir and redirect target
            new_target_list = []
            for target in self.target_list:
                if ".." in target:
                    new_target_list.append(os.path.normpath(os.path.join(old_dir, target)))
                elif os.path.exists(target):
                    new_target_list.append(target)
            self.target_list = new_target_list

    def print_top_line(self):
        print(self.wdir.resume(), end="")
        print(" [", end="", flush=True)
        first = True
        for unit in self.wdir.unit_list:
            if first:
                first = False
            else:
                print(" ", end="", flush=True)
            unit.result = Execution.run_unit(self.wdir.solver, unit)
            print(ExecutionResult.get_symbol(unit.result), end="", flush=True)
        print("]")

    def print_diff(self):
        if self.param.diff_mode == DiffMode.QUIET:
            return
        
        results = [unit.result for unit in self.wdir.unit_list]
        if not ExecutionResult.EXECUTION_ERROR in results and not ExecutionResult.WRONG_OUTPUT in results:
            return
        
        if not self.param.compact:
            print(self.wdir.unit_list_resume())
        
        if self.param.diff_mode == DiffMode.FIRST:
        # printing only the first wrong case
            wrong = [unit for unit in self.wdir.unit_list if unit.result != ExecutionResult.SUCCESS][0]
            if self.param.is_up_down:
                print(Diff.mount_up_down_diff(wrong))
            else:
                print(Diff.mount_side_by_side_diff(wrong))
            return

        if self.param.diff_mode == DiffMode.ALL:
            for unit in self.wdir.unit_list:
                if unit.result != ExecutionResult.SUCCESS:
                    if self.param.is_up_down:
                        print(Diff.mount_up_down_diff(unit))
                    else:
                        print(Diff.mount_side_by_side_diff(unit))

    def build_wdir(self) -> bool:
        try:
            self.wdir = Wdir().set_target_list(self.target_list).set_cmd(self.exec_cmd).build().filter(self.param)
        except CompilerError as e:
            print(e)
            return False
        except FileNotFoundError as e:
            print(e)
            return False
        return True

    def missing_target(self) -> bool:
        # no solver and no test cases
        if self.wdir.solver is None and len(self.wdir.unit_list) == 0:
            print(colour("red", "fail: ") + "No solver or tests found.")
            return True
        return False
    
    def list_mode(self) -> bool:
        # list mode
        if self.wdir.solver is None and len(self.wdir.unit_list) > 0:
            print(Report.centralize(" No solvers found. Listing Test Cases ", "╌"), flush=True)
            print(self.wdir.resume())
            print(self.wdir.unit_list_resume())
            return True
        return False

    def free_run(self) -> bool:
        # free run mode
        if self.wdir.solver is not None and len(self.wdir.unit_list) == 0:
            print(Report.centralize(" No test cases found. Running: " + self.wdir.solver.executable + " ", symbols.hbar), flush=True)
            # force print to terminal
            Runner.free_run(self.wdir.solver.executable)
            return True
        return False

    def diff_mode(self) -> bool:
        print(Report.centralize(" Running solver against test cases ", "═"))
        self.print_top_line()
        self.print_diff()

class Build:

    def __init__(self, target_out: str, source_list: List[str], param: Param.Manip, to_force: bool):
        self.target_out = target_out
        self.source_list = source_list
        self.param = param
        self.to_force = to_force

    def execute(self):
        try:
            wdir = Wdir().set_sources(self.source_list).build()
            wdir.manipulate(self.param)
            Writer.save_target(self.target_out, wdir.unit_list, self.to_force)
        except FileNotFoundError as e:
            print(str(e))
            return False
        return True


tko_guide = """
       ╔════ TKO GUIA COMPACTO ════╗
╔══════╩═════ BAIXAR PROBLEMA ═════╩═══════╗
║        tko down <curso> <label>          ║
║ exemplo poo  : tko down poo carro        ║
║ exemplo fup  : tko down fup opala        ║
╟─────────── EXECUTAR SEM TESTAR ──────────╢
║          tko run <cod, cod...>           ║
║exemplo ts  : tko run solver.ts           ║
║exemplo cpp : tko run main.cpp lib.cpp    ║
╟──────────── RODAR OS TESTES ─────────────╢
║   tko run cases.tio <cod, ...> [-i ind]  ║
║ exemplo: tko run cases.tio main.ts       ║
║só ind 6: tko run cases.tio main.c -i 6   ║
╟── DEFINIR EXTENSÃO PADRÃO DOS RASCUNHOS ─╢
║           tko config -l <ext>            ║
║     exemplo c : tko config -l c          ║
║  exemplo java : tko config -l java       ║
╟─────────── MUDAR VISUALIZAÇÃO ───────────╢
║             tko config <--opcao>         ║
║DiffMode: tko config [--side  | --updown ]║
║Cores   : tko config [--mono  | --color  ]║
║Encoding: tko config [--ascii | --unicode]║
╚══════════════════════════════════════════╝
"""

bash_guide = """
       ╔═══ BASH  GUIA COMPACTO ════╗
╔══════╩════ MOSTRAR E NAVEGAR ═════╩══════╗
║Mostrar arquivos  : ls                    ║
║Mostrar ocultos   : ls -la                ║
║Mudar de pasta    : cd _nome_da_pasta     ║
║Subir um nível    : cd ..                 ║
╟─────────────── CRIAR ────────────────────╢
║Criar um arquivo  : touch _nome_do_arquivo║
║Criar uma pasta   : mkdir _nome_da_pasta  ║
╟─────────────── REMOVER ──────────────────╢
║Apagar um arquivo : rm _nome_do_arquivo   ║
║Apagar uma pasta  : rm -r _nome_da_pasta  ║
║Renomear ou mover : mv _antigo _novo      ║
╟─────────────── CONTROLAR ────────────────╢
║Últimos comandos  : SETA PRA CIMA         ║
║Limpar console    : Control L             ║
║Cancelar execução : Control C             ║
║Finalizar entrada : Control D             ║
╚══════════════════════════════════════════╝
"""
#!/usr/bin/env python3



class Task:
    def __init__(self):
        self.line_number = 0
        self.line = ""
        self.key = ""
        self.grade = ""
        self.skills = []
        self.title = ""
        self.link = ""

    def get_grade(self):
        if self.grade == "":
            return red(GSym.uncheck)
        if self.grade == "x":
            return green(GSym.check)
        number = int(self.grade)
        if number < 7:
            return red(GSym.numbers[number])
        return yellow(GSym.numbers[number])

    def get_percent(self):
        if self.grade == "":
            return 0
        if self.grade == "x":
            return 100
        return int(self.grade) * 10

    def is_done(self):
        return (
            self.grade == "x"
            or self.grade == "7"
            or self.grade == "8"
            or self.grade == "9"
        )

    def set_grade(self, grade):
        valid = ["", "x", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if grade in valid:
            self.grade = grade
            return
        if grade == "0":
            self.grade = ""
            return
        if grade == "10":
            self.grade = "x"
            return
        print(f"Grade inválida: {grade}")

    def __str__(self):
        return f"{self.line_number} : {self.key} : {self.grade} : {self.title} : {self.skills} : {self.link}"

    @staticmethod
    def parse_item_with_link(line) -> Tuple[bool, str, str]:
        pattern = r"\ *-.*\[(.*?)\]\((.+?)\)"
        match = re.match(pattern, line)
        if match:
            return (True, match.group(1), match.group(2))
        return (False, "", "")
    
    @staticmethod
    def parse_task_with_link(line) -> Tuple[bool, str, str]:
        pattern = r"\ *- \[ \].*\[(.*?)\]\((.+?)\)"
        match = re.match(pattern, line)
        if match:
            return (True, match.group(1), match.group(2))
        return (False, "", "")
    

    def load_html_tags(self, line) -> Tuple[bool, List[str]]:
        pattern = r"<!--\s*(.*?)\s*-->"
        match = re.match(pattern, line)
        if not match:
            return (False, [])
        tags_raw = match.group(1).strip()
        tags = [tag.strip() for tag in tags_raw.split()]
        for t in tags:
            if t.startswith("s:"):
                self.skills.append(t[2:])
            elif t.startswith("@"):
                self.key = t[1:]

    @staticmethod
    def parse_arroba_from_title_link(titulo, link) -> Tuple[bool, str]:
        pattern = r"@(\w+)"
        match = re.match(pattern, titulo)
        if not match:
            return (False, "")
        key = match.group(1)
        if not "key/Readme.md" in link:
            return (False, "")
        return (True, key)


    def process_link(self, base_file):
        if self.link.startswith("http"):
            return
        if self.link.startswith("./"):
            self.link = self.link[2:]
        # todo trocar / por \\ se windows
        self.link = base_file + self.link

    # - [Titulo com @palavra em algum lugar](link/@palavra/Readme.md) <!-- tag1 tag2 tag3 -->
    def parse_coding_task(self, line, line_num):
        if line == "":
            return False
        line = line.lstrip()

        found, titulo, link = Task.parse_task_with_link(line)
        if not found:
            return False

        found, key = Task.parse_arroba_from_title_link(titulo, link)
        if not found:
            return False

        self.line = line
        self.line_number = line_num
        self.key = key
        self.title = titulo
        self.link = link

        self.load_html_tags(line)

        return True
    

    # se com - [ ], não precisa das tags dentro do html, o key será dado pelo título
    # se tiver as tags dentro do html, se alguma começar com @, o key será dado por ela
    # - [ ] [Título](link)
    # - [ ] [Título](link) <!-- tag1 tag2 tag3 -->
    # - [Título](link) <!-- tag1 tag2 tag3 -->
    def parse_reading_task(self, line, line_num):
        if line == "":
            return False
        line = line.lstrip()

        
        found, titulo, link = Task.parse_task_with_link(line)
        if found:
            self.key = link
            self.title = titulo
            self.link = link
            self.line = line
            self.line_number = line_num
            self.load_html_tags(line)
            return True
        
        found, titulo, link = Task.parse_item_with_link(line)
        self.key = ""
        if found:
            self.load_html_tags(line)
            if self.key == "":
                return False
            self.title = titulo
            self.link = link
            self.line = line
            self.line_number = line_num
            return True

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
        self.group = ""
        self.requires = []
        self.requires_ptr = []
        self.type = "main"

    def __str__(self):
        return f"linha={self.line_number} : {self.key} : {self.title} : {self.skills} : {self.requires} : {self.mdlink} : {[t.key for t in self.tasks]}"

    def is_complete(self):
        return all([t.is_done() for t in self.tasks])

    def get_percent(self):
        total = len(self.tasks)
        if total == 0:
            return 0
        done = sum([t.get_percent() for t in self.tasks])
        return done // total

    def in_progress(self):
        if self.is_complete():
            return False
        for t in self.tasks:
            if t.grade != "":
                return True
        return False

    def not_started(self):
        if self.is_complete():
            return False
        if self.in_progress():
            return False
        return True

    def is_reachable(self, cache):
        if self.key in cache:
            return cache[self.key]

        if len(self.requires_ptr) == 0:
            cache[self.key] = True
            return True
        cache[self.key] = all(
            [r.is_complete() and r.is_reachable(cache) for r in self.requires_ptr]
        )
        return cache[self.key]

    def parse_quest(self, line, line_num):
        pattern = r"^#+\s*(.*?)<!--\s*(.*?)\s*-->\s*$"
        match = re.match(pattern, line)
        titulo = None
        tags = []

        if match:
            titulo = match.group(1)
            tags_raw = match.group(2).strip()
            tags = [tag.strip() for tag in tags_raw.split()]
        else:
            pattern = r"^#+\s*(.*?)\s*$"
            match = re.match(pattern, line)
            if match:
                titulo = match.group(1)
                tags.append("@" + get_md_link(titulo))
            else:
                return False

        try:
            key = [t[1:] for t in tags if t.startswith("@")][0]
            self.line = line
            self.line_number = line_num
            self.title = titulo
            self.skills = [t[2:] for t in tags if t.startswith("s:")]
            self.requires = [t[2:] for t in tags if t.startswith("r:")]
            self.mdlink = "#" + get_md_link(titulo)
            groups = [t[2:] for t in tags if t.startswith("g:")]
            if len(groups) > 0:
                self.group = groups[0]
            else:
                self.group = ""
            type = [t for t in tags if t.startswith("t:")]
            if len(type) > 0:
                self.type = type[0][2:]
            self.key = key
            return True
        except Exception as e:
            print(e)
            return False


def rm_comments(title: str) -> str:
    if "<!--" in title and "-->" in title:
        title = title.split("<!--")[0] + title.split("-->")[1]
    return title


def get_md_link(title: str) -> str:
    if title is None:
        return ""
    title = title.lower()
    out = ""
    for c in title:
        if c == " " or c == "-":
            out += "-"
        elif c == "_":
            out += "_"
        elif c.isalnum():
            out += c
    return out


class Game:
    def __init__(self, file: Optional[str] = None):
        self.clusters: Dict[str, List[Quest]] = {}  # quests indexed by group
        self.clusters[""] = []
        self.cluster_order: List[str] = [""]  # order of clusters
        self.quests: Dict[str, Quest] = {}  # quests indexed by quest key
        self.tasks: Dict[str, Task] = {}  # tasks  indexed by task key
        if file is not None:
            self.parse_file(file)

    def get_task(self, key: str) -> Task:
        if key in self.tasks:
            return self.tasks[key]
        raise Exception(f"fail: task {key} not found in course definition")

    def load_group(self, line, line_num) -> Tuple[bool, Optional[str]]:
        pattern = r"^#+\s*(.*?)<!--\s*(.*?)\s*-->\s*$"
        match = re.match(pattern, line)
        titulo = None
        tags = []

        if match:
            titulo = match.group(1)
            tags_raw = match.group(2).strip()
            tags = [tag.strip() for tag in tags_raw.split(" ")]
            if "group" in tags:
                return (True, titulo)
        return (False, None)

    def load_quest(self, line, line_num) -> Tuple[bool, Optional[Quest]]:
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

    def load_task(self, line, line_num, last_quest) -> bool:
        if line == "":
            return False
        task = Task()
        found = False
        if task.parse_reading_task(line, line_num + 1):
            found = True
        if task.parse_coding_task(line, line_num + 1):
            found = True
        if not found:
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

        # verify is there are keys repeated between quests, tasks and groups

        keys = [k for k in self.clusters.keys()] +\
               [k for k in self.quests.keys()] +\
               [k for k in self.tasks.keys()]

        # print chaves repetidas
        for k in keys:
            if keys.count(k) > 1:
                print(f"Chave repetida: {k}")
                exit(1)

        # remove all quests without tasks
        valid_quests = {}
        for k, q in self.quests.items():
            if len(q.tasks) > 0:
                valid_quests[k] = q

        self.quests = valid_quests

        # for q in self.quests.values():
        #   if len(q.tasks) == 0:
        #     print(f"Quest {q.key} não tem tarefas")
        #     exit(1)

        for q in self.quests.values():
            for r in q.requires:
                if r in self.quests:
                    q.requires_ptr.append(self.quests[r])
                else:
                    print(f"Quest\n{str(q)}\nrequer {r} que não existe")
                    exit(1)

        # check if there is a cycle

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

    def parse_file(self, file):
        lines = open(file).read().split("\n")
        last_quest = None
        active_group = ""
        for index, line in enumerate(lines):
            found, group = self.load_group(line, index)
            if found:
                active_group = group
                continue

            found, quest = self.load_quest(line, index)
            if found:
                last_quest = quest
                quest.group = active_group
                if quest.group not in self.clusters:
                    self.clusters[quest.group] = []
                    self.cluster_order.append(quest.group)
                self.clusters[quest.group].append(quest)
                continue

            self.load_task(line, index, last_quest)

        self.validate_requirements()
        for t in self.tasks.values():
            t.process_link(os.path.dirname(file) + "/")

    def get_reachable_quests(self):
        # cache needs to be reseted before each call
        cache = {}
        return [q for q in self.quests.values() if q.is_reachable(cache)]

    def show_quests(self):
        print(
            f"Quests de Entrada: {[q.key for q in self.quests.values() if len(q.requires) == 0]}"
        )
        print(f"Total de quests: {len(self.quests)}")
        print(f"Total de tarefas: {len(self.tasks)}")
        print(f"Total de clusters: {len(self.clusters)}")
        # print("\n".join([str(q) for q in self.quests.values()]))

    def generate_graph(self, output):
        saida = []
        saida.append(f"@startuml {output}")
        saida.append("digraph diag {")
        saida.append('  node [style="rounded,filled", shape=box]')

        def info(q):
            return f'"{q.title.strip()}:{len(q.tasks)}"'

        for q in self.quests.values():
            token = "->"
            if len(q.requires_ptr) > 0:
                for r in q.requires_ptr:
                    saida.append(f"  {info(r)} {token} {info(q)}")
            else:
                v = '  "Início"'
                saida.append(f"{v} {token} {info(q)}")

        for q in self.quests.values():
            if q.type == "main":
                saida.append(f"  {info(q)} [fillcolor=lime]")
            else:
                saida.append(f"  {info(q)} [fillcolor=pink]")

        groups = {}
        for q in self.quests.values():
            if q.group == "":
                continue
            if q.group not in groups:
                groups[q.group] = []
            groups[q.group].append(q)

        for c in groups.values():
            if c == "":
                continue
            saida.append(f"  subgraph cluster_{c[0].group} {{")
            saida.append(f'    label="{c[0].group}"')
            saida.append(f"    style=filled")
            saida.append(f"    color=lightgray")
            for q in c:
                saida.append(f"    {info(q)}")

            saida.append("  }")

        saida.append("}")
        saida.append("@enduml")
        saida.append("")

        open(output + ".puml", "w").write("\n".join(saida))
        subprocess.run(["plantuml", output + ".puml", "-tsvg"])



class Play:
    cluster_prefix = "'"

    def __init__(self, game: Game, rep: RepoSettings, repo_alias: str, fnsave):
        self.fnsave = fnsave
        self.repo_alias = repo_alias
        self.help_options = 4
        self.help_index = 0
        self.rep = rep
        self.show_link = "link" in self.rep.view
        self.show_done = "done" in self.rep.view
        self.show_init = "init" in self.rep.view
        self.show_todo = "todo" in self.rep.view

        help = [v for v in self.rep.view if v.startswith("help_")]
        if len(help) > 0:
            self.help_index = int(help[0][5:])
            if self.help_index >= self.help_options:
                self.help_index = 0
        else:
            self.help_index = 0

        self.show_perc = "perc" in self.rep.view
        self.show_fold = not "unfold" in self.rep.view
        self.show_hack = "hack" in self.rep.view
        self.show_view = "view" in self.rep.view

        if not self.show_done and not self.show_init and not self.show_todo:
            self.show_done = True
            self.show_init = True
            self.show_todo = True

        self.game: Game = game

        self.clusters: Dict[str, str] = self.find_cluster_keys()
        self.clusters_keys = {}
        for k, v in self.clusters.items():
            self.clusters_keys[v] = k
        self.tasks: Dict[str, Task] = {}  # visible tasks  indexed by upper letter
        self.quests: Dict[str, Quest] = {}  # visible quests indexed by number
        self.active: List[str] = []  # expanded quests

        for k, v in self.rep.quests.items():
            if "e" in v:
                self.active.append(k)

        self.term_limit = 130

        for key, grade in rep.tasks.items():
            if key in game.tasks:
                game.tasks[key].set_grade(grade)

    def read_link(self, link):
        if link.endswith(".md"):
            if link.startswith("https"):
                with tempfile.NamedTemporaryFile(delete=False) as f:
                    file = f.name
                    cfg = RemoteCfg()
                    cfg.from_url(link)
                    cfg.download_absolute(file)
                    link = file
                    # verify is subprocess succeeds
            result = subprocess.run(["glow", "-p", link])
            if result.returncode != 0:
                print(f"Erro ao abrir o arquivo {link}")
                print("Verifique se o arquivo está no formato markdown")
                input("Digite enter para continuar")

    def down_task(self, task: Task):
        if task.key in task.title:
            print(f"Tarefa de código {task.key}")
            cmd = red(f"tko down {self.repo_alias} {task.key}")
            print(f"Baixando com o comando {cmd}")
            result = Down.download_problem(self.repo_alias, task.key, None)
            # result = subprocess.run(["tko", "down", self.repo_alias, task.key])
            if result:
                pasta = red(f"{os.getcwd()}/{task.key}/Readme.md")
                print(f"Tarefa baixada na pasta {pasta}")
        else:
            print(f"Essa não é uma tarefa de código")
        input("Digite enter para continuar")

    def save_to_json(self):
        self.rep.quests = {}
        for q in self.active:
            self.rep.quests[q] = "e"
        self.rep.tasks = {}
        for t in self.game.tasks.values():
            if t.grade != "":
                self.rep.tasks[t.key] = t.grade
        self.rep.view = []
        if self.show_link:
            self.rep.view.append("link")
        if self.show_perc:
            self.rep.view.append("perc")
        if not self.show_fold:
            self.rep.view.append("unfold")
        if self.show_hack:
            self.rep.view.append("hack")
        if self.show_view:
            self.rep.view.append("view")
        if self.show_done:
            self.rep.view.append("done")
        if self.show_init:
            self.rep.view.append("init")
        if self.show_todo:
            self.rep.view.append("todo")

        self.rep.view.append(f"help_{self.help_index}")

        self.fnsave()

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
        quests = []
        if self.show_hack:
            quests = self.game.quests.values()
        else:
            quests = self.game.get_reachable_quests()

        reach_keys = []
        reach_keys = [q.key for q in quests]
        menu_keys = [q.key for q in self.quests.values()]

        for key in menu_keys:
            if key not in reach_keys:
                self.quests = {}
                break

        if len(self.quests) == 0:
            index = 0
            for q in quests:
                self.quests[str(index)] = q
                index += 1
        else:
            index = len(self.quests.keys())
            for q in quests:
                if q.key not in menu_keys:
                    self.quests[str(index)] = q
                    index += 1

        # self.active = set([k for k in self.active if k in reach_keys])

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
        if len(titles) > 0:
            max_title = max([len(t) for t in titles])
        return max_title

    def to_show_quest(self, quest: Quest):
        if quest.is_complete() and not self.show_done:
            return False
        if quest.not_started() and not self.show_todo:
            return False
        if quest.in_progress() and not self.show_init:
            return False
        return True

    def get_number(self, value):
        if value >= 0 and value <= 20:
            return GSym.numbers[value]
        return "*"

    def str_quest(self, entry, q, max_title, term_size) -> str:
        resume = ""
        opening = GSym.right
        if q.key in self.active:
            opening = GSym.down
        done = len([t for t in q.tasks if t.is_done()])
        size = len(q.tasks)
        done = self.get_number(done)
        size = self.get_number(size)
        if self.show_perc:
            text = f"{str(q.get_percent()).rjust(2)}%"
            if q.get_percent() == 100:
                text = GSym.check * 3
        else:
            text = f"{str(done)}/{str(size)}"
        space = " " if len(entry) == 1 else ""
        if q.get_percent() == 100:
            resume = cyan(text)
        elif q.is_complete():
            resume = green(text)
        elif q.in_progress():
            resume = yellow(text)
        else:
            resume = red(text)
        entry = colour("b", entry) if q.type == "main" else colour("m", entry)
        qlink = ""
        if self.show_link:
            if term_size > self.term_limit:
                qlink = " " + colour("c", q.mdlink)
            else:
                qlink = "\n      " + colour("c", q.mdlink)
        if not self.to_show_quest(q):
            return ""
        title = q.title
        if self.show_link and term_size > self.term_limit:
            title = title.strip().ljust(max_title + 1)
        extra = ""
        if self.show_fold:
            extra = ""
        title = title.strip()
        return f"{space}{entry} {opening} {resume} {extra}{title}"

    def str_task(self, t, max_title, letter, term_size) -> str:
        vindex = str(letter).rjust(2, " ")
        vdone = t.get_grade()
        vlink = ""
        title = t.title
        if self.show_link:
            if t.key in t.title:
                vlink = red(t.link)
            else:
                vlink = yellow(t.link)
            if term_size > self.term_limit:
                title = t.title.strip().ljust(max_title + 1)
                vlink = " " + vlink
            else:
                vlink = "\n" + vlink
        extra = ""
        if self.show_fold:
            extra = ""
#        title = colour("uline", title)
        return f"  {vindex}  {vdone}  {extra}{title}{vlink}"

    def sort_keys(self, keys):
        single = [k for k in keys if len(str(k)) == 1]
        double = [k for k in keys if len(str(k)) == 2]
        return sorted(single) + sorted(double)

    def print_cluster(self, cluster_name: str, lines: List[str]):
        cluster_key = self.clusters_keys[cluster_name]
        opening = GSym.right
        if cluster_name in self.active:
            opening = GSym.down
        intro = [Color.remove_colors(l).strip().split(" ")[0] for l in lines]
        quests = [v for v in intro if v.isdigit()]
        total = len(quests)
        init = yellow(self.get_number(len([v for v in quests if self.quests[v].in_progress()])))
        done = green(self.get_number(len([v for v in quests if self.quests[v].is_complete()])))
        todo = red(self.get_number(len([v for v in quests if self.quests[v].not_started()])))
        margin = len(cluster_key)
        title = colour_bold("red", cluster_name.strip()[:margin]) + colour("bold", cluster_name.strip()[margin:])
        if total > 0:
            print(f" {opening} {done}/{init}/{todo} {title}")
            if cluster_name in self.active:
                for line in lines:
                    print(line)

    def find_cluster_keys(self) -> Dict[str, str]:
        data = sorted(self.game.cluster_order)
        keys = []
        for cluster in data:
            i = 2
            while (True):
                key = cluster[:i]
                if key not in keys:
                    keys.append(key)
                    break
                i += 1
        output = {}
        for k, v in zip(keys, data):
            output[k] = v
        return output



    def show_options(self):
        term_size = shutil.get_terminal_size().columns
        max_title = self.calculate_pad()
        index = 0

        clusters: Dict[str, List[str]] = {}

        for entry in self.sort_keys(self.quests.keys()):
            quest_output: List[str] = []
            q = self.quests[entry]
            quest_output.append(self.str_quest(entry, q, max_title, term_size))
            if q.key in self.active and self.to_show_quest(q):
                for t in q.tasks:
                    letter = self.calc_letter(index)
                    quest_output.append(self.str_task(t, max_title, letter, term_size))
                    index += 1
                    self.tasks[letter] = t

            if self.show_fold:
                if len(quest_output) > 0:
                    if q.group not in clusters:
                        clusters[q.group] = []
                    clusters[q.group] += [line for line in quest_output if line != ""]
            else:
                for line in quest_output:
                    if line != "":
                        print(line)

        if self.show_fold:
            for group in self.game.cluster_order:
                if group in clusters.keys():
                    self.print_cluster(group, clusters[group])
        return

    @staticmethod
    def get_num_num(s):
        pattern = r"^(\d+)-(\d+)$"
        match = re.match(pattern, s)
        if match:
            return int(match.group(1)), int(match.group(2))
        else:
            return (None, None)

    @staticmethod
    def get_letter_letter(s):
        pattern = r"([a-zA-Z]+)-([a-zA-Z]+)"
        match = re.match(pattern, s)
        if match:
            print(match.group(1), match.group(2))
            return match.group(1), match.group(2)
        return (None, None)

    def expand_range(self, line) -> List[str]:
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
                limits = range(start_index, end_index + 1)
                expand += [self.calc_letter(i) for i in limits]
            else:
                expand.append(t)
        return expand

    def clear(self):
        # subprocess.run("clear")
        pass

    def is_number(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def process_colapse(self):
        all_tasks_closed = True
        for v in self.active:
            if v not in self.clusters.values():
                all_tasks_closed = False
                break
        if all_tasks_closed:
            self.active = []
        else:
            self.active = [q for q in self.active if q in self.clusters.values()]

    def process_expand(self):
        self.update_reachable()
        # verify if all clusters are expanded
        all_clusters_expanded = True
        for k in self.clusters.values():
            if k not in self.active:
                all_clusters_expanded = False
                break
        clusters = [k for k in self.clusters.values()]
        if all_clusters_expanded:
            quests = [q.key for q in self.quests.values()]
            self.active = quests + clusters
        else:
            self.active = self.active + clusters

    def process_down(self, actions):
        for t in actions[1:]:
            if t in self.tasks:
                self.down_task(self.tasks[t])
            else:
                print(f"Tarefa {t} não encontrada")
                input()

    def process_clusters(self, actions):
        for t in actions:
            if t in self.clusters:
                key = self.clusters[t]
                if key not in self.active:
                    print(f"Expandindo {key}")
                    self.active.append(key)
                else:
                    print(f"Contraindo {key}")
                    self.active.remove(key)
            else:
                print(f"{t} não processado")
                input("Digite enter para continuar")

    def process_quests(self, actions):
        for t in actions:
            if not self.is_number(t) or not t in self.quests:
                print(f"{t} não processado")
                input("Digite enter para continuar")
            else:
                key = self.quests[t].key
                if key not in self.active:
                    self.active.append(key)
                    continue
                else:
                    self.active.remove(key)
                    continue
    
    def process_tasks(self, actions):
        for t in actions:
            letter = "".join([c for c in t if c.isupper() and not c.isdigit()])
            number = "".join([c for c in t if c.isdigit()])
            if letter in self.tasks:
                t = self.tasks[letter]
                if len(number) > 0:
                    t.set_grade(number)
                else:
                    if t.grade == "":
                        t.set_grade("x")
                    else:
                        t.set_grade("")
            else:
                print(f"{t} não processado")
                input("Digite enter para continuar")
    
    def process_see(self, actions):
        if len(actions) > 1:
            if actions[1] in self.tasks:
                # print(self.tasks[actions[1]].link)
                self.read_link(self.tasks[actions[1]].link)
            else:
                print(f"{actions[1]} não processado")
                input("Digite enter para continuar")

    def take_actions(self, actions):
        if len(actions) == 0:
            return
        cmd = actions[0]

        if cmd == "<":
            self.process_colapse()

        elif cmd == ">":
            self.process_expand()

        elif cmd == "m" or cmd == "man":
            self.clear()
            self.show_help()
        elif cmd == "c" or cmd == "cmd":
            self.help_index = (self.help_index + 1) % self.help_options
        elif cmd == "f" or cmd == "full":
            self.show_done = True
            self.show_init = True
            self.show_todo = True
        elif cmd == "i" or cmd == "init":
            self.show_done = False
            self.show_init = True
            self.show_todo = False
        elif cmd == "d" or cmd == "done":
            self.show_done = True
            self.show_init = False
            self.show_todo = False
        elif cmd == "t" or cmd == "todo":
            self.show_done = False
            self.show_init = False
            self.show_todo = True
        elif cmd == "l" or cmd == "link":
            self.show_link = not self.show_link
        elif cmd == "p" or cmd == "perc":
            self.show_perc = not self.show_perc
        elif cmd == "j" or cmd == "join":
            self.show_fold = not self.show_fold
        elif cmd == "h" or cmd == "hack":
            self.show_hack = not self.show_hack
        elif cmd == "v" or cmd == "view":
            self.show_view = not self.show_view
        elif cmd == "g" or cmd == "get":
            self.process_down(actions)
        elif len(cmd) >= 2 and cmd[0].isupper() and cmd[1].islower():
            self.process_clusters(actions)
        elif self.is_number(cmd):
            self.process_quests(actions)
        elif cmd[0].isupper():
            self.process_tasks(actions)
        elif cmd == "s" or cmd == "see":
            self.process_see(actions)
        else:
            print(f"{cmd} não processado")
            input("Digite enter para continuar")

    def show_help(self):
        print(
            "Digite "
            + red("t")
            + " os números ou intervalo das tarefas para (marcar/desmarcar), exemplo:"
        )
        print(green("play $ ") + "t 1 3-5")
        input("Digite enter para continuar")

    def show_header(self):
        self.clear()
        ball = self.show_done and self.show_init and self.show_todo
        show_ajuda = green("Digite ") + red("c") + green(" para ajuda")

        full_count = len([q for q in self.quests.values()])
        done_count = len([q for q in self.quests.values() if q.is_complete()])
        init_count = len([q for q in self.quests.values() if q.in_progress()])
        todo_count = len([q for q in self.quests.values() if q.not_started()])

        def checkbox(value):
            return green(GSym.vcheck) if value else yellow(GSym.vuncheck)

        vall = red("full") + (green(GSym.vcheck) if ball else yellow(GSym.vuncheck))
        vdone = "(" + str(done_count).rjust(2, "0") + ")" + red("done") + checkbox(not ball and self.show_done)
        vinit = "(" + str(init_count).rjust(2, "0") + ")" + red("init") + checkbox(not ball and self.show_init)
        vtodo = "(" + str(todo_count).rjust(2, "0") + ")" + red("todo") + checkbox(not ball and self.show_todo)
        vlink = red("link") + ( checkbox(self.show_link) )
        vperc = red("perc") + ( checkbox(self.show_perc) )
        vjoin = red("join") + ( checkbox(self.show_fold) )
        vhack = red("hack") + ( checkbox(self.show_hack) )

        nomes_verm = green("Os nomes em vermelho são comandos")
        prime_letr = green("Basta a primeira letra do comando")
        cluster = red("<LETRA><letra>") + cyan(" {Re Ve} ") + yellow("(Ver Grupo)")
        numeros = red("<Número>") + cyan(" {3 5} ") + yellow("(Ver Quest)")
        todas = red("<") + " ou " + red(">") + yellow(" (Ocultar/Revelar Tudo)")
        letras = red("<LETRA>") + cyan(" {A C-E}") + yellow("(Marcar Tarefa)")
        graduar = red("<LETRA><Valor>") + cyan(" {A0 B5} ") + yellow("(Dar nota)")
        read = red("see <LETRA>") + cyan(" {s B}") + yellow(" (Ler no terminal)")
        down = red("get <LETRA>") + cyan(" {g B}") + yellow(" (Baixar tarefa)")
        cmds = red("cmd") + yellow("  (Visualizar os comandos)")
        manu = red("man") + yellow("  (Mostrar manual detalhado)")
        sair = red("quit") + yellow(" (Sair do programa)")

        sall  = red("full") + yellow(" (Mostrar todas as tarefas)")
        sdone = red("done") + yellow(" (Mostrar tarefas concluídas)")
        sinit = red("init") + yellow(" (Mostrar tarefas em andamento)")
        stodo = red("todo") + yellow(" (Mostrar tarefas não iniciadas)")
        fold  = red("join") + yellow(" (Juntar em categorias)")
        link  = red("link") + yellow(" (Mostrar links das tarefas)")
        hack  = red("hack") + yellow(" (Dá acesso a todas as tarefas)")
        perc  = red("perc") + yellow(" (Mostrar porcentagens)")

        indicadores = f"{vall} {vdone} {vinit} {vtodo}"
        visoes = f"{vjoin}     {vlink}     {vperc}     {vhack}"

        elementos = []
        if self.help_index == 0:
            intro = show_ajuda + " (1/2/3)" + green(" - ") + red("view") + checkbox(self.show_view)
            elementos = [ intro ] + ([ indicadores, visoes ] if self.show_view else [])
        elif self.help_index == 1:
            intro = show_ajuda + " (" + yellow("1") + "/2/3)" + green(" - ") + red("view") + checkbox(self.show_view)
            elementos = [ intro ] + ([ indicadores, visoes ] if self.show_view else [])
            elementos += [ nomes_verm, prime_letr, todas, cluster, numeros, letras, graduar ]
        elif self.help_index == 2:
            intro = show_ajuda + " (1/" + yellow("2") + "/3)" + green(" - ") + red("view") + checkbox(self.show_view)
            elementos = [ intro ] + ([ indicadores, visoes ] if self.show_view else [])
            elementos += [ cmds, manu, down, read, sair ]
        elif self.help_index == 3:
            intro = show_ajuda + " (1/2/" + yellow("3") + ")" + green(" - ") + red("view") + checkbox(self.show_view)
            elementos = [ intro ] + ([ indicadores, visoes ] if self.show_view else [])
            elementos += [sall, sdone, sinit, stodo, fold, perc, link, hack ]
        self.print_elementos(elementos)

    def print_elementos(self, elementos):
        term_size = shutil.get_terminal_size().columns
        maxlen = max([len(Color.remove_colors(t)) for t in elementos])
        qtd = term_size // (maxlen + 3)

        count = 0
        for i in range(len(elementos)):
            print(Color.ljust(elementos[i], maxlen), end="")
            count += 1
            if count >= qtd:
                count = 0
                print("")
            elif i < len(elementos) - 1:
                print(" ║ ", end="")
        if count != 0:
            print("")
        print("")

    def play(self):
        while True:
            self.tasks = {}
            self.update_reachable()
            self.show_header()
            self.show_options()
            print("\n" + green("play$") + " ", end="")
            line = input()
            if line != "" and "quit".startswith(line):
                break
            actions = self.expand_range(line)
            self.take_actions(actions)
            self.save_to_json()

__version__ = "0.4.3"




class MRep:
    @staticmethod
    def list(args):
        sp = SettingsParser()
        settings = sp.load_settings()
        print(f"SettingsFile\n- {sp.settings_file}")
        print(str(settings))

    @staticmethod
    def add(args):
        sp = SettingsParser()
        settings = sp.load_settings()
        if args.url:
            rep = RepoSettings().set_url(args.url)
        elif args.file:
            rep = RepoSettings().set_file(args.file)
        settings.reps[args.alias] = rep
        sp.save_settings()
    
    @staticmethod
    def rm(args):
        sp = SettingsParser()
        settings = sp.load_settings()
        if args.alias in settings.reps:
            settings.reps.pop(args.alias)
            sp.save_settings()
        else:
            print("Repository not found.")

    @staticmethod
    def reset(args):
        sp = SettingsParser()
        sp.settings = Settings()
        sp.save_settings()

    @staticmethod
    def graph(args):
        sp = SettingsParser()
        settings = sp.load_settings()
        rep = settings.get_repo(args.alias)
        file = rep.get_file()
        game = Game()
        game.parse_file(file)
        game.check_cycle()
        game.generate_graph("graph")

class Main:
    @staticmethod
    def run(args):
        PatternLoader.pattern = args.pattern
        param = Param.Basic().set_index(args.index)
        if args.quiet:
            param.set_diff_mode(DiffMode.QUIET)
        elif args.all:
            param.set_diff_mode(DiffMode.ALL)
        else:
            param.set_diff_mode(DiffMode.FIRST)

        if args.filter:
            param.set_filter(True)
        if args.compact:
            param.set_compact(True)

        # load default diff from settings if not specified
        if not args.sideby and not args.updown:
            local = SettingsParser().load_settings().local
            updown = local.updown
            size_too_short = Report.get_terminal_size() < local.sideto_min
            param.set_up_down(updown or size_too_short)
        elif args.sideby:
            param.set_up_down(False)
        elif args.updown:
            param.set_up_down(True)
        run = Run(args.target_list, args.cmd, param)
        run.execute()

    @staticmethod
    def build(args):
        PatternLoader.pattern = args.pattern
        manip = Param.Manip().set_unlabel(args.unlabel).set_to_sort(args.sort).set_to_number(args.number)
        build = Build(args.target, args.target_list, manip, args.force)
        build.execute()
    
    @staticmethod
    def settings(args):
        sp = SettingsParser()
        settings = sp.load_settings()
        
        if args.ascii:
            settings.local.ascii = True
            print("Encoding mode now is: ASCII")
        if args.unicode:
            settings.local.ascii = False
            print("Encoding mode now is: UNICODE")
        if args.mono:
            settings.local.color = False
            print("Color mode now is: MONOCHROMATIC")
        if args.color:
            settings.local.color = True
            print("Color mode now is: COLORED")
        if args.side:
            settings.local.updown = False
            print("Diff mode now is: SIDE_BY_SIDE")
        if args.updown:
            settings.local.updown = True
            print("Diff mode now is: UP_DOWN")
        if args.lang:
            settings.local.lang = args.lang
            print("Default language extension now is:", args.lang)
        if args.ask:
            settings.local.lang = "ask"
            print("Language extension will be asked always.")
        if args.show:
            print(sp.get_settings_file())
            print(str(settings.local))
        sp.save_settings()

    @staticmethod
    def play(args):
        if args.repo:
            print("playing repo", args.repo)
            sp = SettingsParser()
            settings = sp.load_settings()
            repo = settings.get_repo(args.repo)
            game = Game()
            file = repo.get_file()
            game.parse_file(file)
            #passsing a lambda function to the play class to save the settings
            play = Play(game, repo, args.repo, lambda: sp.save_settings())
            play.play()

    @staticmethod
    def down(args):
        Down.download_problem(args.course, args.activity, args.language)

class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='tko', description='A tool for competitive programming.')        
        self.subparsers = self.parser.add_subparsers(title='subcommands', help='help for subcommand.')
        self.add_parser_args()
        self.add_parent_basic()
        self.add_parent_manip()
        self.add_parser_run()
        self.add_parser_build()
        self.add_parser_down()
        self.add_parser_config()
        self.add_parser_repo()
        self.add_parser_play()

    def add_parser_args(self):
        self.parser.add_argument('-c', metavar='CONFIG_FILE', type=str, help='config json file.')
        self.parser.add_argument('-w', metavar='WIDTH', type=int, help="terminal width.")
        self.parser.add_argument('-v', action='store_true', help='show version.')
        self.parser.add_argument('-g', action='store_true', help='show tko simple guide.')
        self.parser.add_argument('-b', action='store_true', help='show bash simple guide.')
        self.parser.add_argument('-m', action='store_true', help='monochromatic.')

    def add_parent_basic(self):
        parent_basic = argparse.ArgumentParser(add_help=False)
        parent_basic.add_argument('--index', '-i', metavar="I", type=int, help='run a specific index.')
        parent_basic.add_argument('--pattern', '-p', metavar="P", type=str, default='@.in @.sol',
                                  help='pattern load/save a folder, default: "@.in @.sol"')
        self.parent_basic = parent_basic
    
    def add_parent_manip(self):
        parent_manip = argparse.ArgumentParser(add_help=False)
        parent_manip.add_argument('--width', '-w', type=int, help="term width.")
        parent_manip.add_argument('--unlabel', '-u', action='store_true', help='remove all labels.')
        parent_manip.add_argument('--number', '-n', action='store_true', help='number labels.')
        parent_manip.add_argument('--sort', '-s', action='store_true', help="sort test cases by input size.")
        parent_manip.add_argument('--pattern', '-p', metavar="@.in @.out", type=str, default='@.in @.sol',
                                  help='pattern load/save a folder, default: "@.in @.sol"')
        self.parent_manip = parent_manip

    def add_parser_run(self):
        parser_r = self.subparsers.add_parser('run', parents=[self.parent_basic], help='run with test cases.')
        parser_r.add_argument('target_list', metavar='T', type=str, nargs='*', help='solvers, test cases or folders.')
        parser_r.add_argument('--filter', '-f', action='store_true', help='filter solver in temp dir before run')
        parser_r.add_argument('--compact', '-c', action='store_true', help='Dont show case descriptions in failures')
        parser_r.add_argument("--cmd", type=str, help="bash command to run code")

        group_n = parser_r.add_mutually_exclusive_group()
        group_n.add_argument('--quiet', '-q', action='store_true', help='quiet mode, do not show any failure.')
        group_n.add_argument('--all', '-a', action='store_true', help='show all failures.')

        # add a exclusive group for diff mode
        group = parser_r.add_mutually_exclusive_group()
        group.add_argument('--updown', '-u', action='store_true', help="diff mode up-to-down.")
        group.add_argument('--sideby', '-s', action='store_true', help="diff mode side-by-side.")
        parser_r.set_defaults(func=Main.run)

    def add_parser_build(self):
        parser_b = self.subparsers.add_parser('build', parents=[self.parent_manip], help='build a test target.')
        parser_b.add_argument('target', metavar='T_OUT', type=str, help='target to be build.')
        parser_b.add_argument('target_list', metavar='T', type=str, nargs='+', help='input test targets.')
        parser_b.add_argument('--force', '-f', action='store_true', help='enable overwrite.')
        parser_b.set_defaults(func=Main.build)

    def add_parser_down(self):
        parser_d = self.subparsers.add_parser('down', help='download problem from repository.')
        parser_d.add_argument('course', type=str, nargs='?', help=" [ fup | ed | poo ].")
        parser_d.add_argument('activity', type=str, nargs='?', help="activity @label.")
        parser_d.add_argument('--language', '-l', type=str, nargs='?', help="[ c | cpp | js | ts | py | java ]")
        parser_d.set_defaults(func=Main.down)

    def add_parser_config(self):
        parser_s = self.subparsers.add_parser('config', help='settings tool.')
        parser_s.add_argument('--show',  '-s', action='store_true', help='show current settings.')

        g_encoding = parser_s.add_mutually_exclusive_group()
        g_encoding.add_argument('--ascii', action='store_true',    help='set ascii mode.')
        g_encoding.add_argument('--unicode', action='store_true', help='set unicode mode.')

        g_color = parser_s.add_mutually_exclusive_group()
        g_color.add_argument('--color', action='store_true', help='set colored mode.')
        g_color.add_argument('--mono',  action='store_true', help='set mono    mode.')
        

        g_diff = parser_s.add_mutually_exclusive_group()
        g_diff.add_argument('--side', action='store_true', help='set side_by_side diff mode.')
        g_diff.add_argument('--updown', action='store_true', help='set up_to_down   diff mode.')


        g_lang = parser_s.add_mutually_exclusive_group()
        g_lang.add_argument("--lang", '-l', metavar='ext', type=str, help="set default language extension.")
        g_lang.add_argument("--ask", action='store_true', help='ask language extension every time.')

    def add_parser_repo(self):
        parser_repo = self.subparsers.add_parser('repo', help='manipulate repositories.')
        subpar_repo = parser_repo.add_subparsers(title='subcommands', help='help for subcommand.')

        repo_list = subpar_repo.add_parser('list', help='list all repositories')
        repo_list.set_defaults(func=MRep.list)

        repo_add = subpar_repo.add_parser('add', help='add a repository.')
        repo_add.add_argument('alias', metavar='alias', type=str, help='alias of the repository to be added.')
        repo_add.add_argument('--url', type=str, help='add a repository url to the settings file.')
        repo_add.add_argument('--file', type=str, help='add a repository file to the settings file.')
        repo_add.set_defaults(func=MRep.add)

        repo_rm = subpar_repo.add_parser('rm', help='remove a repository.')
        repo_rm.add_argument('alias', metavar='alias', type=str, help='alias of the repository to be removed.')
        repo_rm.set_defaults(func=MRep.rm)

        repo_reset = subpar_repo.add_parser('reset', help='reset all repositories to factory default.')
        repo_reset.set_defaults(func=MRep.reset)

        repo_graph = subpar_repo.add_parser('graph', help='generate graph of the repository.')
        repo_graph.add_argument('alias', metavar='alias', type=str, help='alias of the repository to be graphed.')
        repo_graph.set_defaults(func=MRep.graph)

    def add_parser_play(self):
        parser_p = self.subparsers.add_parser('play', help='play a game.')
        parser_p.add_argument('repo', metavar='repo', type=str, help='repository to be played.')
        parser_p.set_defaults(func=Main.play)

    def main(self):
        args = self.parser.parse_args()

        if len(sys.argv) == 1:
            self.parser.print_help()
            return
        if args.w is not None:
            Report.set_terminal_size(args.width)
        if args.c:
            SettingsParser.user_settings_file = args.c
        settings = SettingsParser().load_settings()
        if settings.local.ascii:
            symbols.set_ascii()
        else:
            symbols.set_unicode()
        if not args.m and settings.local.color:
            Color.enabled = True
            symbols.set_colors()

        if args.v or args.g or args.b:
            if args.v:
                print("tko version " + __version__)
            if args.b:
                print(bash_guide[1:], end="")
            if args.g:
                print(tko_guide[1:], end="")
        else:
            try:
                args.func(args)
            except ValueError as e:
                print(str(e))

def main():
    try:
        parser = Parser()
        parser.main()
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nKeyboard Interrupt")
        sys.exit(1)

if __name__ == '__main__':
    main()

