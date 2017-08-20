"""Creates the file structure for the project."""

from pathlib import Path


def make_file_structure(
        project_name: str, parent: Path, bin_project: bool=False):
    """Creates the base file structure for the project.

    Parameters
    ----------
    project_name : str
        User supplied name for the project.
    parent : pathlib.Path
        A path to the folder where the project will be created.
    bin_project : bool
        If True, a binary folder will be created.
    """
    project_dir = parent / project_name
    project_dir.mkdir()
    module = make_module(project_dir)
    docs = project_dir / 'docs'
    tests = project_dir / 'tests'
    for directory in [docs, tests]:
        directory.mkdir()
    if bin_project:
        bin_d = project_dir / 'bin'
        bin_d.mkdir()
    return


def make_module(project_dir: Path) -> Path:
    """Makes the module folder and assoicated files."""
    module = project_dir / project_dir.name
    module.mkdir()
    return module
