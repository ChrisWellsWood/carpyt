"""Creates the file structure for the project."""

import os
from pathlib import Path

import yaml


TEMPLATES = Path(os.path.abspath(__file__)).parent / 'templates'


class Directory:
    """Represents a directory in the filesystem."""

    def __init__(self, name, content):
        self.name = name
        self.content = content


class File:
    """Represents a file in the filesystem."""

    def __init__(self, name, content):
        self.name = name
        self.content = content


def run_template_parser(root_template: Path) -> Directory:
    """Parses a file structure template.

    Parameters
    ----------
    root_template : pathlib.Path
        Base template for the file structure.

    Returns
    -------
    file_tree : Directory
        The file structure generated from the templates.

    Raises
    ------
    RecursionError
        Raised if a recusive template structure is detected.
    """
    with open(str(root_template), 'r') as rtf:
        raw_template = yaml.load(rtf)
    return Directory('top', list(map(parse_template, raw_template.items())))


def parse_template(template: ((str, str), dict)):
    """Parses a template.

    Parameters
    ----------
    template : dict
        A file structure template.

    Returns
    -------
    file_structure : Directory or File
        The file structure created by parsing the template.
    """
    print(template)
    (entry_type, name), contents = template
    if entry_type == 'file':
        return File(name, contents)
    elif entry_type == 'dir':
        return Directory(name, list(map(parse_template, contents.items())))
