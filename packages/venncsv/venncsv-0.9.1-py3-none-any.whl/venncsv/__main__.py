#!/usr/bin/python3

# imports

from .__init__ import __doc__ as description, __version__ as version
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from warnings import simplefilter
from sys import argv
from libfunx import get_source, get_target
from os.path import split as pathsplit

# globals

class args: pass # container for arguments

def venncsv(argv):
    """'$ venncsv x.csv y.csv' then writes x_and_y.csv, x_or_y.csv, x_xor_y.csv, x_minus_y.csv and y_minus_y.csv."""

    parser = Parser(prog='venncsv', formatter_class=Formatter, description=description) # get arguments
    parser.add_argument('-V', '--version', action='version', version='venncsv ' + version)
    parser.add_argument('-v', '--verbose', action='store_true', help='show what happens')
    parser.add_argument('-y', '--yes',  action='store_true', help='overwrite existing target files (default: ask)')
    parser.add_argument('-n', '--no',  action='store_true', help='don\'t overwrite existing target files (default: ask)')
    parser.add_argument('-a', '--x-and-y',   action='store_true', help='write <input1>_and_<input2>.csv')
    parser.add_argument('-o', '--x-or-y',    action='store_true', help='write <input1>_or_<input2>.csv')
    parser.add_argument('-x', '--x-xor-y',   action='store_true', help='write <input1>_xor_<input2>.csv')
    parser.add_argument('-m', '--x-minus-y', action='store_true', help='write <input1>_minus_<input2>.csv')
    parser.add_argument('-w', '--y-minus-x', action='store_true', help='write <input2>_minus_<input1>.csv')
    parser.add_argument('input1')
    parser.add_argument('input2')
    parser.parse_args(argv[1:], args)
    if not (args.x_and_y or args.x_or_y or args.x_xor_y or args.x_minus_y or args.y_minus_x):
        args.x_and_y, args.x_or_y, args.x_xor_y, args.x_minus_y, args.y_minus_x = 5 * [True]

    def read_csv(input):
        input = get_source(input, '.csv')
        head = None
        rows = set()
        for line in open(input):
            line = line.rstrip()
            if head is None:
                head = line
            elif line:
                rows.add(line)
        if head is None:
            exit(f'Header not found in input file {input!r}')
        if not head:
            exit(f'Empty header in input file {input!r}')
        if args.verbose:
            print(f'{len(rows)} rows <-- {input!r}')
        return head, rows

    head1, rows1 = read_csv(args.input1)
    head2, rows2 = read_csv(args.input2)
    if head1 != head2:
        exit('Input file headers don\'t match')
    
    def write_csv(input1, op, input2, rows):
        input1 = pathsplit(input1)[-1]
        input2 = pathsplit(input2)[-1]
        target = get_target(f'{input1[:-4]}_{op}_{input2}', '.csv', yes=args.yes, no=args.no)
        with open(target, 'w') as output:
            print(head1, file=output)
            for row in sorted(rows):
                print(row, file=output)
        if args.verbose:
            print(f'{len(rows)} rows --> {target!r}')

    if args.x_and_y:   write_csv(args.input1, 'and',   args.input2, rows1 & rows2)
    if args.x_or_y:    write_csv(args.input1, 'or',    args.input2, rows1 | rows2)
    if args.x_xor_y:   write_csv(args.input1, 'xor',   args.input2, rows1 ^ rows2)
    if args.x_minus_y: write_csv(args.input1, 'minus', args.input2, rows1 - rows2)
    if args.y_minus_x: write_csv(args.input2, 'minus', args.input1, rows2 - rows1)

def main():
    try:
        simplefilter('ignore')
        venncsv(argv)
    except KeyboardInterrupt:
        print()

if __name__ == '__main__':
    main()

