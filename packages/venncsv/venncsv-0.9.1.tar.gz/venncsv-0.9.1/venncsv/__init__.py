#!/usr/bin/python3

"""'$ venncsv x.csv y.csv' writes x_and_y.csv, x_or_y.csv, x_xor_y.csv, x_minus_y.csv and y_minus_y.csv.

Let's have two CSV files, say x.csv and y.csv. Each file contains a header and zero or more rows.

File extensions must be underscore '.csv'. The two headers must be equal.

Rows in the two input files are intended as two sets of strings. No field splitting is performed.

If we issue:

    $ venncsv -aoxmw x.csv y.csv

or simply:

    $ venncsv x.csv y.csv

then we generate five files, as follows:

    x_and_y.csv   contains x & y, the intersection of x and y, the rows both in x and y
    x_or_y.csv    contains x | y, the union of x and y, the rows in x or y or both
    x_xor_y.csv   contains x ^ y, the exclusive union of x and y, the rows in x or y but not in both
    x_minus_y.csv contains x - y, the difference between x and y, the rows in x but not in y
    y_minus_x.csv contains y - x, the difference between y and x, the rows in y but not in x

                   ┌───────────┐
                   │ x - y     │
                 x │   ┌───────┼───┐
                   │   │ x & y │   │
                   └───┼───────┘   │ y
                       │     y - x │
                       └───────────┘

Sets x - y, x & y and y - x are the three wedges of the Venn diagram of sets x and y,
and hence the 'venncsv' name.

Files to be generated can be selected by -a -o -x -m and -w flags, but if no such flag is given
then all five files are written.

Trailing blanks in header and rows are stripped. Empty rows and duplicated rows are skipped.

Rows in output files are alphabetically sorted.

Input files can be prefixed by a path, but output files are always written in the current directory.
"""

__version__ = '0.9.1'

__requires__ = ['libfunx']

