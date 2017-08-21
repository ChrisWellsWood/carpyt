"""Creates the file structure for the project."""

import os
from pathlib import Path

import yaml


TEMPLATES = Path(os.path.abspath(__file__)).parent / 'templates'


def make_file_structure(
        project_name: str, parent_dir: Path, bin_project: bool=False):
    """Creates the base file structure for the project.

    Parameters
    ----------
    project_name : str
        User supplied name for the project.
    parent_dir : pathlib.Path
        A path to the folder where the project will be created.
    bin_project : bool
        If True, a binary folder will be created.
    """
    project_dir = make_project_dir(parent_dir, project_name)
    module_dir = make_module_dir(project_dir)
    docs_dir = make_docs_dir(project_dir)
    tests_dir = make_tests_dir(project_dir)
    if bin_project:
        bin_dir = make_bin_dir(project_dir)
    return


def create_from_template(directory: Path, template_item: (str, str),
                         required_fields: dict=None):
    """Creates a file from a template item."""
    file_name, file_info = template_item
    (directory / file_name).touch()
    return


def make_project_dir(parent_dir: Path, project_name: str) -> Path:
    """Makes the module folder and associated files."""
    project_dir = parent_dir / project_name
    project_dir.mkdir()
    with open(str(TEMPLATES / 'project.yml'), 'r') as inf:
        project_template = yaml.load(inf)
    for template_item in project_template.items():
        create_from_template(project_dir, template_item)
    return project_dir


def make_module_dir(project_dir: Path) -> Path:
    """Makes the module folder and associated files."""
    module_dir = project_dir / project_dir.name
    module_dir.mkdir()
    init_path = module_dir / '__init__.py'
    init_path.touch()
    return module_dir


def make_docs_dir(project_dir: Path) -> Path:
    """Makes the docs folder and associated files."""
    docs_dir = project_dir / 'docs'
    docs_dir.mkdir()
    return docs_dir


def make_tests_dir(project_dir: Path) -> Path:
    """Makes the tests folder and associated files."""
    tests_dir = project_dir / 'tests'
    tests_dir.mkdir()
    return tests_dir


def make_bin_dir(project_dir: Path) -> Path:
    """Makes the bin folder and assoicated files."""
    bin_dir = project_dir / 'bin'
    bin_dir.mkdir()
    return bin_dir
