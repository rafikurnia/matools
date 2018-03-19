#!/usr/bin/env python
from arg_parser import create_parser


def main():
    parser = create_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except TypeError:
        parser.print_help()


if __name__ == "__main__":
    main()
