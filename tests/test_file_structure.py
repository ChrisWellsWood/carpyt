"""Tests for creating file structure."""

from pathlib import Path
from unittest import TestCase
import tempfile

from carpyt.file_structure import make_file_structure


class TestFileCreation(TestCase):
    """Tests that all required files are generated correctly."""

    def test_lib_creation(self):
        """Makes sure that the base lib directory structure is created."""
        with tempfile.TemporaryDirectory() as test_dir:
            test_dir_path = Path(test_dir)
            project_name = 'lovely_project'
            make_file_structure(project_name, test_dir_path)
            project = test_dir_path / project_name
            module = project / project.name
            docs = project / 'docs'
            tests = project / 'tests'
            for directory in [project, module, tests, docs]:
                self.assertTrue(directory.exists())
            bin_d = project / 'bin'
            self.assertFalse(bin_d.exists())

    def test_bin_creation(self):
        """Makes sure that the base bin directory structure is created."""
        with tempfile.TemporaryDirectory() as test_dir:
            test_dir_path = Path(test_dir)
            project_name = 'lovely_project'
            make_file_structure(project_name, test_dir_path, bin_project=True)
            project = test_dir_path / project_name
            module = project / project_name
            docs = project / 'docs'
            tests = project / 'tests'
            bin_d = project / 'bin'
            for directory in [project, module, tests, docs, bin_d]:
                self.assertTrue(directory.exists())