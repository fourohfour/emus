class EmusColumn:
    def __init__(self, head, entries):
        self.head = head
        self.entries = entries

    def header(self):
        return self.head

    def row(self, arg):
        return self.entries.get(arg, None)

    __getitem__ = row

    def rows(self):
        return iter(self.entries.items())

    __iter__ = rows

    def __str__(self):
        return self.header()

class EmusRow:
    def __init__(self, head, entries):
        self.head = head
        self.entries = entries

    def header(self):
        return self.head

    def column(self, arg):
        return self.entries.get(arg, None)

    __getitem__ = column

    def columns(self):
        return iter(self.entries.items())

    __iter__ = columns

    def __str__(self):
        return self.header()

class EmusTable:
    def __init__(self, table):
        self._table = table

    def title(self):
        return self._table.title

    def column(self, arg):
        if arg not in self._table.col_heads:
            raise ValueError("No such column {}".format(arg))
        else:
            column_entries = {}
            col_id = self._table.col_heads.index(arg)
            for entry in self._table.entries:
                if entry[0] == col_id:
                    entry_row = self._table.row_heads[entry[1]]
                    column_entries[entry_row] = entry[2]

            return EmusColumn(arg, column_entries)

    __getitem__ = column

    def row(self, arg):
        if arg not in self._table.row_heads:
            raise ValueError("No such row {}".format(arg))
        else:
            row_entries = {}
            row_id = self._table.row_heads.index(arg)
            for entry in self._table.entries:
                if entry[1] == row_id:
                    entry_col = self._table.col_heads[entry[0]]
                    row_entries[entry_col] = entry[2]

            return EmusRow(arg, row_entries)

    def rows(self):
        for row in self._table.row_heads:
            yield self.row(row)

    def columns(self):
        for col in self._table.col_heads:
            yield self.column(col)

    __iter__ = columns

    def __str__(self):
        return self.title()

class EmusRepresentation:
    def __init__(self, tables):
        self._tables = tables

    def table(self, arg):
        for table in self._tables:
            if table.title == arg:
                return EmusTable(table)
        else:
            return None

    __getitem__ = table

    def tables(self):
        for table in self._tables:
            yield EmusTable(table)

    __iter__ = tables

class Emitter:
    def __init__(self, outfile, representation):
        self._outfile = outfile
        self._repr    = representation

    def output_file(self):
        return self._outfile

    def data(self):
        return self._repr

    def emit(self):
        raise NotImplemented()


