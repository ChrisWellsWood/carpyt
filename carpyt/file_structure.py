"""Creates the file structure for the project."""

import os
from pathlib import Path

import yaml


TEMPLATES = Path(os.path.abspath(__file__)).parent / 'templates'


class BasePlan:
    """Base class for the plan objects."""
    def __init__(self, name, content, labels=None):
        if labels:
            self.name = name.format(**{
                k[1:-1]:v
                for k, v in labels.items()})
        else:
            self.name = name
        self.content = content

    def __getitem__(self, item):
        return self.content[item]


class DirectoryPlan(BasePlan):
    """Represents a directory in the filesystem.
    
    Parameters
    ----------
    name : str
        Name of the directory.
    content : [DirectoryPlan or FilePlan]
        A list of fies of directories in the directory.
    labels : dict, optional
        A dictionary of labels that can be used to customise directory
        names on file structure creation.
    """
    def __repr__(self):
        rep_str = "<Directory Plan: name='{}'>".format(self.name)
        return rep_str

    def make(self, host_dir, recursive=True):
        """Makes the directory.
        
        Parameters
        ----------
        host_dir : pathlib.Path
            Path to the parent directory of this plan.
        recursive : bool, optional
            If True, make will be called on all the contents objects.
        """
        dir_path = host_dir / self.name
        dir_path.mkdir()
        if recursive and (self.content is not None):
            for template_item in self.content:
                template_item.make(dir_path)
        return


class FilePlan(BasePlan):
    """Represents a file in the filesystem.
    
    Parameters
    ----------
    name : str
        Name of the file.
    content : str
        The contents of the file, as a string.
    labels : dict, optional
        A dictionary of labels that can be used to customise file
        names on file structure creation.
    """
    def __repr__(self):
        rep_str = "<File Plan: name='{}'>".format(self.name)
        return rep_str

    def make(self, host_dir):
        """Makes the file.

        Parameters
        ----------
        host_dir : pathlib.Path
            Path to the parent directory of this plan.
        """
        file_path = host_dir / self.name
        file_path.touch()
        return


def run_template_parser(root_template, template_name=None, directory_stack=None,
                        parsed_templates=None, labels=None):
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
            parse_item(template_item, directory_stack, parsed_templates,
                       labels=labels))
    return DirectoryPlan(name, parse_tree, labels=labels)


def parse_item(template, directory_stack=None, parsed_templates=None,
               labels=None):
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
    if directive == 'link':
        external_template = Path(content['path'])
        template_name = name if name else external_template.stem
        return run_template_parser(
            external_template, template_name, directory_stack, parsed_templates,
            labels=labels)
    if directory_stack:
        directory_stack.append(name)
    else:
        directory_stack = [name]
    if directive == 'file':
        return FilePlan(name, content, labels=labels)
    elif directive == 'dir':
        if content is None:
            return DirectoryPlan(name, content, labels=labels)
        else:
            parse_tree = []
            for template_item in sorted(content.items()):
                parse_tree.append(
                    parse_item(template_item, directory_stack,
                               parsed_templates, labels=labels))
            return DirectoryPlan(name, parse_tree, labels=labels)
    else:
        raise ValueError('Unknown directive. Options: dir, external, file')
