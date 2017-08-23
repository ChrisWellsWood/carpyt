"""Tests for creating file structure."""

import os
from pathlib import Path
from unittest import TestCase

from carpyt import parse_template


TEST_TEMPLATES = Path(os.path.abspath(__file__)).parent / 'test_templates'


class TestTemplateParsing(TestCase):
    """Tests that templates are parsed correctly."""

    def test_std_template(self):
        """Tests the creation of a simple parse tree."""
        template_path = TEST_TEMPLATES / 'simple.yml'
        file_tree = parse_template(template_path)
        for exp_file in ['setup.py', 'requirements.txt', '{module_name}/']:
            self.assertTrue(exp_file in file_tree)
        return

    def test_nested_template(self):
        """Tests creation of nested parse tree."""
        template_path = TEST_TEMPLATES / 'nested_parent.yml'
        file_tree = parse_template(template_path)
        for exp_file in ['setup.py', 'requirements.txt', '{module_name}/']:
            self.assertTrue(exp_file in file_tree)
        return


class TestFileCreation(TestCase):
    """Tests that all required files are generated correctly."""
