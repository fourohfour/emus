import interface

class TextEmitter(interface.Emitter):
    def textify(self, table):
        col_widths = {}
        for col in table.columns():
            col_widths[str(col)] = len(str(col))
            for row, value in col:
                if len(str(value)) > col_widths[str(col)]:
                    col_widths[str(col)] = len(str(value))

        s = "|"
        score = "|"
        rh_width = 0

        for row in table.rows():
            if len(str(row)) > rh_width:
                rh_width = len(str(row))

        rh_width += 1

        s += (" " * rh_width) + "|"
        score += ("-" * rh_width)

        for col in table.columns():
            s += "{head: <{w}}|".format(head = str(col), w = col_widths[str(col)])
            score += "+" + ("-" * col_widths[str(col)])
        score += "|\n"
        hborder = "+" +  "-" * (len(score) - 3) + "+\n"

        s  = hborder + s + "\n" + score

        for row in table.rows():
            s += "|{head: <{rhw}}|".format(head = str(row), rhw = rh_width)
            for col in table.columns():
                s += "{val: <{w}}|".format(val = row[str(col)], w = col_widths[str(col)])
            s += "\n"

        s  += hborder

        return s


    def emit(self):
        for table in self.data():
            str_table = self.textify(table)
            self.output_file().write("\n")
            self.output_file().write(str_table)
            self.output_file().write("\n")


