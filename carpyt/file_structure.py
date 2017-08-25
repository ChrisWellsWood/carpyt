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


def run_template_parser(root_template, template_name=None, directory_stack=None,
                        parsed_templates=None):
    """Parses a file structure template.

    Parameters
    ----------
    root_template : pathlib.Path
        Base template for the file structure.
    name : str, optional
        Name for the base folder, if none then the stem of the
        path to the template is used instead.
    directory_stack : [str], optional
        Directory stack.

    Returns
    -------
    parse_tree : DirectoryPlan
        The file structure generated from the templates.

    Raises
    ------
    RecursionError
        Raised if a recursive template structure is detected.
    """
    root_template = root_template.resolve()
    if parsed_templates:
        if str(root_template) in parsed_templates:
            raise RecursionError(
                'This file has already been parsed in this branch, that '
                'means that the file structure would be recursive and '
                'thus keep making directories forever! Best change that.')
        else:
            parsed_templates.append(str(root_template))
    else:
        parsed_templates = [str(root_template)]
    name = template_name if template_name else root_template.stem
    if directory_stack:
        directory_stack.append(name)
    else:
        directory_stack = [name]
    with open(str(root_template), 'r') as rtf:
        raw_template = yaml.load(rtf)
    parse_tree = []
    for template_item in sorted(raw_template.items()):
        parse_tree.append(
            parse_item(template_item, directory_stack, parsed_templates))
    return DirectoryPlan(name, parse_tree)


def parse_item(template, directory_stack=None, parsed_templates=None):
    """Parses a template item.

    Parameters
    ----------
    template : dict
        A file structure template.
    directory_stack : [str], optional
        Directory stack.

    Returns
    -------
    file_structure : DirectoryPlan or FilePlan
        The file structure created by parsing the template.

    Raises
    ------
    ValueError
        Raised if an unknown directive is raised.
    """
    (directive, name), content = template
    if directive == 'file':
        return FilePlan(name, content)
    elif directive == 'link':
        external_template = Path(content['path'])
        template_name = name if name else external_template.stem
        return run_template_parser(
            external_template, template_name, directory_stack, parsed_templates)
    elif directive == 'dir':
        if directory_stack:
            directory_stack.append(name)
        else:
            directory_stack = [name]
        if content is None:
            return DirectoryPlan(name, content)
        else:
            parse_tree = []
            for template_item in sorted(content.items()):
                parse_tree.append(
                    parse_item(template_item, directory_stack,
                               parsed_templates))
            return DirectoryPlan(name, parse_tree)
    else:
        raise ValueError('Unknown directive. Options: dir, external, file')
