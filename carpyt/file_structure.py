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


def run_template_parser(root_template: Path, name=None) -> DirectoryPlan:
    """Parses a file structure template.

    Parameters
    ----------
    root_template : pathlib.Path
        Base template for the file structure.

    Returns
    -------
    parse_tree : DirectoryPlan
        The file structure generated from the templates.

    Raises
    ------
    RecursionError
        Raised if a recusive template structure is detected.
    """
    with open(str(root_template), 'r') as rtf:
        raw_template = yaml.load(rtf)
    parse_tree = list(map(parse_template, sorted(raw_template.items())))
    return DirectoryPlan(name if name is not None else root_template.stem,
                         parse_tree)


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

    Raises
    ------
    ValueError
        Raised if an unknown directive is raised.
    """
    print(template)
    (directive, name), content = template
    if directive == 'file':
        return FilePlan(name, content)
    elif directive == 'link':
        external_template = Path(content['path'])
        return run_template_parser(external_template, name)
    elif directive == 'dir':
        if content is None:
            return DirectoryPlan(name, content)
        else:
            return DirectoryPlan(
                name, list(map(parse_template, sorted(content.items()))))
    else:
        raise ValueError('Unknown directive. Options: dir, external, file')
