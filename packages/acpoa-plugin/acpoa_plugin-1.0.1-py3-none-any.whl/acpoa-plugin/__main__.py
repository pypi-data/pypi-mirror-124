import argparse
import os
import sys


def hyphenated(string: str) -> str:
    return '-'.join([word for word in string.casefold().split()])


parser = argparse.ArgumentParser(description="A ACPOA plugin creation helper", prog="acpoa-plugin")
subparsers = parser.add_subparsers(title="command", required=True, dest="command")

# parse command 'new'
parser_new = subparsers.add_parser('new', description="Create a new plugin directory.")
parser_new.add_argument('name', type=hyphenated, help="Name of the plugin (python package name)")
parser_new.add_argument('path', nargs='?', default=os.getcwd(), help="Path where to create the plugin directory")
parser_new.add_argument('-p', '--pretty-name', help="Set the plugin's pretty name.")
parser_new.add_argument('-u', '--url', help="Main plugin URL")
parser_new.add_argument('-d', '--description', help="Short description of the plugin")
parser_new.add_argument('-v', '--version', default="0.0.1", help="Version of the plugin")
parser_new.add_argument('-a', '--author', help="Author name")
parser_new.add_argument('-e', '--author-email', help="Author email")
parser_new.add_argument('-F', '--force-erase', action="store_true",
                        help="Delete the existing directory before creating the new one.")
parser_new.add_argument('-f', '--force-replace', action="store_true",
                        help="Replace existing files by the default ones.")

# parse command 'build'
parser_build = subparsers.add_parser('build')
parser_build.add_argument('path', nargs='?', default=os.getcwd(), help="Path to the plugin directory")
parser_build.add_argument('-d', '--data-detection', action="store_true",
                          help="Automatically detect data inside your plugin and ad them to the setup.py file so "
                               "they can be packed within your plugin.")

arguments = parser.parse_args(sys.argv[1:])


def new(args: argparse.Namespace):
    from .new import new
    new(args)


def build(args: argparse.Namespace):
    from .build import build
    build(args)


globals()[arguments.command](arguments)
