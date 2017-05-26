#!/usr/bin/python3.5

import sys
from utils import *
import tokeniser
import parser
import interface
import markdown

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

if __name__ == "__main__":

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

    if "h" in switches or "help" in switches:
        print("Emus: Table compiler")
        print("  usage: emus.py input_file [options]")
        print("  options:")
        print("    --md [output_file] Output markdown to output_file")
        print("                       or to stdout if output_file omitted")
        print("    -h, --help         Display this help message")
        sys.exit(0)


    files = list(filter(lambda v: not v.endswith(".py"), switches["root"].values()))

    if not files:
        Error.fatal("Emus", "Argument Error", "parsing args", "No input specified")

    try:
        with open(files[0]) as f:
            tokens = tokeniser.Tokeniser.tokenise(f.read())
            tables = parser.Parser.parse(tokens)
            emusrepr = interface.EmusRepresentation(tables)

            if "md" in switches:
                if not switches["md"].has_nth_value(0):
                    markdown.MarkdownEmitter(sys.stdout, emusrepr).emit()
                else:
                    with open(switches["md"].first_value(), "w") as md_out:
                        markdown.MarkdownEmitter(md_out, emusrepr).emit()
            else:
                Error.warn("Emus", "No Target", "outputting data", "No target specififed")

    except FileNotFoundError:
        Error.fatal("Emus", "Argument Error", "reading input", "Input file not found")

    except IOError:
        Error.fatal("Emus", "IO Error", "reading input", "Unable to open input file")



