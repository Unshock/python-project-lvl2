#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('f', metavar='first_file')
parser.add_argument('s', metavar='second_file')


def main():
    args = parser.parse_args()
    print(args.accumulate(args.integers))


if __name__ == '__main__':
    main()

