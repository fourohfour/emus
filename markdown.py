import interface

class MarkdownEmitter(interface.Emitter):
    def markdownify(self, table):
        s = "### {}\n\n".format(table)
        cols = list(table.columns())
        s += "| |" + "|".join(str(col) for col in cols) + "|\n"
        s += "|:----|" + "|".join([":-------:"] * len(cols)) + "|\n"

        for r in table.rows():
            values = []
            entries = [c for c, e in r]

            rs = "|**{}**|".format(r)
            for c in cols:
                if str(c) in entries:
                    rs += r[str(c)]
                else:
                    rs += " "
                rs += "|"

            rs += "\n"
            s += rs

        return s

    def emit(self):
        self.output_file().write("\n---\n\n")
        for table in self.data():
            str_table = self.markdownify(table)
            self.output_file().write(str_table)
            self.output_file().write("\n---\n\n")
