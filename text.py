import interface

class TableWidth:
    FIRST_COL = -1
    MIN_COL   = 3

    def __init__(self, table):
        col_widths = {TableWidth.FIRST_COL: TableWidth.MIN_COL}

        for row in table.rows():
            row_name = str(row)
            if len(row_name) > col_widths[TableWidth.FIRST_COL]:
                col_widths[TableWidth.FIRST_COL] = len(row_name)

        for col in table.columns():
            col_name = str(col)
            col_widths[col_name] = len(col_name) if len(col_name) > TableWidth.MIN_COL else TableWidth.MIN_COL
            for row, value in col:
                if len(str(value)) > col_widths[col_name]:
                    col_widths[col_name] = len(str(value))

        self.col_widths = col_widths

    def col_width(self, c):
        return self.col_widths[c]

    def first_col_width(self):
        return self.col_width(TableWidth.FIRST_COL)

    def table_width(self):
        return sum(self.col_widths.values()) + len(self.col_widths) + 1


class TextEmitter(interface.Emitter):
    def h_border(self, width):
        return "+" + ("-" * (width.table_width() - 2)) + "+\n"

    def h_title(self, width, table):
        spaces = (width.table_width() // 2) - (len(table.title()) // 2)
        return (" " * spaces) + table.title() + "\n"

    def textify(self, table):
        master = ""
        width = TableWidth(table)
        master += self.h_title(width, table)
        master += self.h_border(width)

        master += "|" + (" " * width.first_col_width()) + "|"
        for col in table.columns():
            cw = width.col_width(str(col))
            master += "{head: <{w}}|".format(head = str(col), w = cw)
        master += "\n"

        col_names = [TableWidth.FIRST_COL] + [str(col) for col in table.columns()]

        master += "|" + "+".join(width.col_width(col) * "-" for col in col_names) + "|\n"

        for row in table.rows():
            master += "|{head: <{fcw}}|".format(head = str(row), fcw = width.first_col_width())
            for col in table.columns():
                col_name = str(col)
                cw = width.col_width(col_name)
                master += "{val: <{w}}|".format(val = row[col_name], w = cw)
            master += "\n"

        master += self.h_border(width)
        return master

    def emit(self):
        for table in self.data():
            str_table = self.textify(table)
            self.output_file().write("\n")
            self.output_file().write(str_table)
            self.output_file().write("\n")


