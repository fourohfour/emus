# emus - Table Compiler

**emus** is a utility for quickly constructing tables in a variety of formats.

## Using emus

### Input

Input to **emus** is given in the form of .emus documents. These documents specify the data in a table in the manner shown in the example below.

    "Airspeed Velocity" {
        -> African :: Laden    => "20 m/s"
        -> African :: Unladen  => "33 m/s"
        -> European:: Laden    => "16 m/s"
        -> European:: Unladen  => "28 m/s"
    }

    "Match Results" {
        -> John   :: "Game 1"   => 2
        -> Andrew :: "Game 1"   => 3
        -> John   :: "Game 2"   => 4
        -> Andrew :: "Game 2"   => 0
    }

A table is specified with a value indicating its title and a pair of braces. Cell entries are given between the braces in the following form:

    -> COL :: ROW => ENTRY

All spacing is purely aesthetic. All values including titles, row and column names, and entries, are strings. Double quotes are needed for values containing spaces or syntactical characters.

### Commands

A command to emus is of the following form:

    emus <input_file> (options)

The `input_file` should be a .emus file. The `options` are mainly to specify how the output should be emitted. A help option (`-h` or `--help`) can also be specified.

### Emitters

All emitters can be specified with a flag and an optional `output_file` as shown below. If no output file is specified the output is printed to stdout.

Example: `emus ./my_data.emus --txt ./output.txt`

---

`--md`: Markdown

Markdown is a common markup language used on GitHub, StackOverflow and Reddit among other places. Although not a feature of standard markdown, many markdown implementations support tables. The `--md` emitter will output tables in this common form. The `--markdown` flag is a supported alias.

`--txt`: Text

This flag allows table output in an 'ascii-art' style. These tables will only display well in environments which use monospaced fonts. The `--text` flag is a supported alias.

---

### Example Usage

Emit the file `scores.emus` as markdown and write to `pretty-scores.md`:

    emus ./scores.emus --md ./pretty-scores.md

Emit the file `rankings.emus` as text to stdout:

    emus ./rankings.emus --txt
