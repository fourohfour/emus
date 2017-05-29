import sys
from .utils import *
from . import tokeniser, parser, interface, markdown, text

help_text = """\

Emus: Table Compiler
  usage: emus.py <input_file> (options)
  options:
      --md [output_file]    Output markdown to output_file
                            or to stdout if output_file omitted

      --txt [output_file]   Output as text to output_file
                            or to stdout if output_file omitted

      --help                Display this help message
"""


def display_help():
    print(help_text)
    sys.exit(0)


class Switch:
    last = "root"

    def __init__(self, name):
        self.name   = name
        Switch.last = name
        self.vals = []

    def add_value(self, v):
        self.vals.append(v)

    def __str__(self):
        return "{}: {}".format(self.name, self.vals)

    def __repr__(self):
        return "Switch({})".format(str(self))

    def has_nth_value(self, n):
        return n < len(self.vals)

    def nth_value(self, n):
        if n >= len(self.vals):
            Error.fatal("Emus", "Argument Error", "parsing args",
                        "Not enough values for switch {}".format(self.name))
        return self.vals[n]

    def first_value(self):
        return self.nth_value(0)

    def values(self):
        return iter(self.vals)

class SwitchManager:
    def __init__(self, switches):
        self.switches = switches
        self.functions = {
                "misc.root"    : ["root"]          ,
                "misc.help"    : ["h", "help"]     ,
                "emit.markdown": ["md", "markdown"],
                "emit.text"    : ["txt", "text"]   ,
        }

    def check(self):
        legal = [sw for fn in self.functions.values() for sw in fn]

        for switch in self.switches:
            if switch not in legal:
                return Result.failure(switch)

        return Result.success(len(self.switches))

    def fulfilled(self, fn):
        for fn_bind in self.functions[fn]:
            if fn_bind in self.switches:
                return True
        return False

    def fulfilling(self, fn):
        for fn_bind in self.functions[fn]:
            if fn_bind in self.switches:
                return self.switches[fn_bind]
        return None

def emit(switch, emitter, emusrepr):
    if not switch.has_nth_value(0):
        emitter(sys.stdout, emusrepr).emit()
    else:
        try:
            with open(switch.first_value(), "w") as emit_out:
                emitter(emit_out, emusrepr).emit()
        except IOError:
            Error.fatal("Emus", "IO Error", "writing output", "Unable to open output file")
            sys.exit(1)

    sys.exit(0)

def switch_manager():
    switches    = {"root": Switch("root")}

    for arg in sys.argv:
        if arg.startswith("--"):
            switch = arg[2:].lower()
            switches[switch] = Switch(switch)

        elif arg.startswith("-"):
            for char in arg[1:]:
                switches[char.lower()] = Switch(char.lower())

        else:
            switches[Switch.last].add_value(arg)

    return SwitchManager(switches)

def main():
    manager = switch_manager()

    switch_check = manager.check()

    if switch_check.is_failure():
        Error.warn("Emus", "Argument Error", "parsing flags",
                   "Flag '{}' does not exist -".format(switch_check.unwrap_err()))
        display_help()

    if manager.fulfilled("misc.help"):
        display_help()

    files = list(manager.fulfilling("misc.root").values())[1:]

    if not files:
        Error.warn("Emus", "Argument Error", "parsing args", "No input specified")
        display_help()

    try:
        with open(files[0]) as f:
            tokens = tokeniser.Tokeniser.tokenise(f.read())
            tables = parser.Parser.parse(tokens)
            emusrepr = interface.EmusRepresentation(tables)

            if manager.fulfilled("emit.markdown"):
                emit(manager.fulfilling("emit.markdown"), markdown.MarkdownEmitter, emusrepr)

            if manager.fulfilled("emit.text"):
                emit(manager.fulfilling("emit.text"), text.TextEmitter, emusrepr)

            else:
                Error.warn("Emus", "No Target", "outputting data", "No target specififed")
                display_help()

    except FileNotFoundError:
        Error.fatal("Emus", "Argument Error", "reading input", "Input file not found")
        sys.exit(1)

    except IOError:
        Error.fatal("Emus", "IO Error", "reading input", "Unable to open input file")
        sys.exit(1)


