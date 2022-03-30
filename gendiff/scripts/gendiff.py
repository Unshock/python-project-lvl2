#!/usr/bin/env python
import argparse
from gendiff.generate_diff import generate_diff

parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file', metavar='first_file')
parser.add_argument('second_file', metavar='second_file')
parser.add_argument('-f', '--format', metavar='FORMAT', help='set format of output')


def main():
    #generate_diff()
    args = parser.parse_args()
    #print(args.accumulate(args.integers))
    print(generate_diff(args.first_file, args.second_file))


if __name__ == '__main__':
    main()

