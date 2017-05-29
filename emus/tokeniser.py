from enum import Enum
from .utils import *

class Token(Enum):
    VALUE  = 0
    ARROW  = 1
    DARROW = 2
    DOTS   = 3
    LBRACE = 4
    RBRACE = 5
    EOF    = 99

def is_reserved(c):
    if c in "-=>:{}\" " or c.isspace():
        return True
    else:
        return False

class Tokeniser:
    FAIL_END = 9000

    def __init__(self, s):
        self.s     = s
        self.back  = 0
        self.front = 0
        self.tokens = []

    def front_cur(self):
        if self.front < len(self.s):
            return Result.success(self.s[self.front])
        else:
            return Result.failure(self.FAIL_END)


    def front_incr(self):
        self.front += 1
        return self.front_cur()

    def front_reject(self):
        self.front -= 1
        return self.front_cur()

    def front_incr_while(self, f):
        result = self.front_cur()
        if result.is_success():
            if not f(result.unwrap()):
                return Result.success("")
        else:
            return result

        while True:
            incr = self.front_incr()
            if incr.is_success():
                if f(incr.unwrap()):
                    continue
                else:
                    self.front_reject()
                    return Result.success("")
            else:
                return incr

    def consume(self):
        start = self.back
        end   = self.front + 1

        self.back  = self.front + 1
        self.front = self.back

        return self.s[start:end]

    def consume_pattern(self, pattern):
        for char in pattern:
            inres = self.front_incr()

            if inres.is_success():
                inchar = inres.unwrap()
                if inchar == char:
                    continue
                else:
                    Error.fatal("Tokeniser", "Syntax Error",
                                "parsing '{}'".format(pattern),
                                "Expected '{}' but found '{}'".format(char, inchar))
            else:
                return inres
        return Result.success(self.consume())

    @classmethod
    def tokenise(cls, s):
        tksr = cls(s)

        while True:
            cur_result = tksr.front_cur()
            if cur_result.is_failure():
                break
            char = cur_result.unwrap()

            if is_reserved(char):
                if char == "-":
                    tok = tksr.consume_pattern(">")
                    if tok.is_success():
                        tksr.tokens.append((Token.ARROW, None))
                    else:
                        if tok.unwrap_err() == tksr.FAIL_END:
                            break

                if char == "=":
                    tok = tksr.consume_pattern(">")
                    if tok.is_success():
                        tksr.tokens.append((Token.DARROW, None))
                    else:
                        if tok.unwrap_err() == tksr.FAIL_END:
                            break

                if char == ":":
                    tok = tksr.consume_pattern(":")
                    if tok.is_success():
                        tksr.tokens.append((Token.DOTS, None))
                        continue
                    else:
                        if tok.unwrap_err() == tksr.FAIL_END:
                            break


                if char == "{":
                    tksr.tokens.append((Token.LBRACE, None))
                    tksr.consume()
                    continue

                if char == "}":
                    tksr.tokens.append((Token.RBRACE, None))
                    tksr.consume()
                    continue

                if char == "\"":
                    if tksr.front_incr().is_failure():
                        break

                    while_result = tksr.front_incr_while(lambda c: not c == "\"")

                    if while_result.is_failure() or tksr.front_incr().is_failure():
                        break

                    tksr.tokens.append((Token.VALUE, tksr.consume().strip("\"")))
                    continue

                tksr.consume()
                continue

            else:
                while_result = tksr.front_incr_while(lambda c: not is_reserved(c))
                if while_result.is_failure():
                    break
                tksr.tokens.append((Token.VALUE, tksr.consume()))
                continue

        tksr.tokens.append((Token.EOF, None))

        #print("\n".join(["{}: {}".format(t[0].name, t[1]) for t in tksr.tokens]))
        return tksr.tokens

