from .utils import *
from .tokeniser import Token

class Table:
    def __init__(self):
        self.title = ""

        self.col_heads   = []
        self.row_heads   = []

        self.entries   = []

    def add_col_header(self, name):
        self.col_heads.append(name)

    def add_row_header(self, name):
        self.row_heads.append(name)

    def add_entry(self, col, row, entry):
        if col not in self.col_heads:
            self.add_col_header(col)

        if row not in self.row_heads:
            self.add_row_header(row)

        col_id = self.col_heads.index(col)
        row_id = self.row_heads.index(row)

        self.entries.append((col_id, row_id, entry))

    def __str__(self):
        s = ""
        for entry in self.entries:
            s += "{}, {}: {}\n".format(self.col_heads[entry[0]], self.row_heads[entry[1]], entry[2])
        return s

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.ptr = 0

        self.tables = {}
        self.next_table_id = 0

    def table(self, table_id):
        return self.tables[table_id]

    def create_table(self, title):
        table_id = self.next_table_id

        self.tables[table_id] = Table()
        self.tables[table_id].title = title

        self.next_table_id += 1
        return table_id

    def expect(self, token_type):
        if self.tokens[self.ptr][0] == token_type:
            r_ptr = self.ptr
            self.ptr += 1
            return Result.success(self.tokens[r_ptr][1])
        else:
            return Result.failure(self.tokens[self.ptr][0])

    def syntax_check(self, result, task, expected):
        if result.is_failure():
            bad_type = result.unwrap_err()
            Error.fatal("Parser", "Syntax Error", task,
                        "Expected '{}', got {}".format(expected, bad_type.name))
        else:
            return result.unwrap()


    @staticmethod
    def is_EOF(result):
        if result.is_success():
            return False

        return result.unwrap_err() == Token.EOF

    def increment(self):
        self.ptr += 1

    def parse_entry(self, table_id):
        self.syntax_check(self.expect(Token.ARROW), "parsing Entry", "->")
        col_val = self.syntax_check(self.expect(Token.VALUE), "parsing Column Value", "VALUE")
        self.syntax_check(self.expect(Token.DOTS), "parsing Dots", "::")
        row_val = self.syntax_check(self.expect(Token.VALUE), "parsing Row Value", "VALUE")
        self.syntax_check(self.expect(Token.DARROW), "parsing Value Arrow", "=>")
        value = self.syntax_check(self.expect(Token.VALUE), "parsing Entry Value", "VALUE")

        self.table(table_id).add_entry(col_val, row_val, value)

    def parse_table(self):
        table_id = -1

        title_res = self.expect(Token.VALUE)

        if title_res.is_success():
            table_id = self.create_table(title_res.unwrap())
        elif Parser.is_EOF(title_res):
            return False
        else:
            self.syntax_check(title_res, "parsing Table Definition", "VALUE")

        brace_res = self.syntax_check(self.expect(Token.LBRACE), "parsing Table Definition", "{{")

        while self.expect(Token.RBRACE).is_failure():
            self.parse_entry(table_id)

        return True


    @classmethod
    def parse(cls, tokens):
        parser = cls(tokens)
        while True:
            if not parser.parse_table():
                break

        return list(parser.tables.values())
