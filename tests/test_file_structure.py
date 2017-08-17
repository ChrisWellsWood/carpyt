"""Tests for creating file structure."""

from pathlib import Path
from unittest import TestCase
import tempfile

from carpyt.file_structure import make_file_structure


class TestFileCreation(TestCase):
    """Tests that all required files are generated correctly."""

    def test_module_creation(self):
        """Makes sure that the base directory structure is created."""
        with tempfile.TemporaryDirectory() as test_dir:
            test_dir_path = Path(test_dir)
            project_name = 'lovely_project'
            make_file_structure(project_name, test_dir_path)
            project_dir = test_dir_path / project_name
            self.assertTrue(project_dir.is_dir())
