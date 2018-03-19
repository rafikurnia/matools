import argparse

from functions import create_all, create_stack_sets, create_stack_instances, delete_all, test


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version="0.0.1")

    subparsers = parser.add_subparsers()

    create_all_parser = subparsers.add_parser("create-all")
    create_all_parser.add_argument("--configfile")
    create_all_parser.set_defaults(func=create_all)

    create_stack_sets_parser = subparsers.add_parser("create-stack-sets")
    create_stack_sets_parser.add_argument("--configfile")
    create_stack_sets_parser.set_defaults(func=create_stack_sets)

    create_stack_instances_parser = subparsers.add_parser("create-stack-instances")
    create_stack_instances_parser.add_argument("--configfile")
    create_stack_instances_parser.set_defaults(func=create_stack_instances)

    delete_all_parser = subparsers.add_parser("delete-all")
    delete_all_parser.add_argument("--configfile")
    delete_all_parser.set_defaults(func=delete_all)

    delete_all_parser = subparsers.add_parser("test")
    delete_all_parser.add_argument("--configfile")
    delete_all_parser.set_defaults(func=test)

    return parser
