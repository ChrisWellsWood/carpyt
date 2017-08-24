"""Creates the file structure for the project."""

import os
from pathlib import Path

import yaml


TEMPLATES = Path(os.path.abspath(__file__)).parent / 'templates'


class DirectoryPlan:
    """Represents a directory in the filesystem."""

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __getitem__(self, item):
        return self.content[item]

    def __repr__(self):
        rep_str = "<Directory Plan: name='{}'>".format(self.name)
        return rep_str


class FilePlan:
    """Represents a file in the filesystem."""

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __getitem__(self, item):
        return self.content[item]

    def __repr__(self):
        rep_str = "<File Plan: name='{}'>".format(self.name)
        return rep_str


def run_template_parser(root_template: Path) -> DirectoryPlan:
    """Parses a file structure template.

    Parameters
    ----------
    root_template : pathlib.Path
        Base template for the file structure.

    Returns
    -------
    file_tree : DirectoryPlan
        The file structure generated from the templates.

    Raises
    ------
    RecursionError
        Raised if a recusive template structure is detected.
    """
    with open(str(root_template), 'r') as rtf:
        raw_template = yaml.load(rtf)
    return DirectoryPlan(root_template.stem,
                         list(map(parse_template, raw_template.items())))


def parse_template(template: ((str, str), dict)):
    """Parses a template.

    Parameters
    ----------
    template : dict
        A file structure template.

    Returns
    -------
    file_structure : DirectoryPlan or FilePlan
        The file structure created by parsing the template.
    """
    (entry_type, name), content = template
    if entry_type == 'file':
        return FilePlan(name, content)
    elif entry_type == 'dir':
        if content is None:
            return DirectoryPlan(name, content)
        else:
            return DirectoryPlan(name, list(map(parse_template, content.items())))
