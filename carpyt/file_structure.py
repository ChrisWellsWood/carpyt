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
    project = parent / project_name
    module = project / project_name
    docs = project / 'docs'
    tests = project / 'tests'
    for directory in [project, module, docs, tests]:
        directory.mkdir()
    if bin_project:
        bin_d = project / 'bin'
        bin_d.mkdir()
    return
