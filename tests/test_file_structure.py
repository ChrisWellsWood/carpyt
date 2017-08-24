"""Tests for creating file structure."""

import os
from pathlib import Path
from unittest import TestCase

import carpyt


TEST_TEMPLATES = Path(os.path.abspath(__file__)).parent / 'test_templates'


class TestTemplateParsing(TestCase):
    """Tests that templates are parsed correctly."""

    def test_simple_template(self):
        """Tests creation of nested parse tree."""
        template_path = TEST_TEMPLATES / 'nested_simple.yml'
        file_tree = carpyt.run_template_parser(template_path)
        self.assertTrue(file_tree.name == 'nested_simple')
        self.assertTrue(file_tree[0].name == '{module}')
        self.assertTrue(file_tree[0][0].name == 'tests')
        self.assertTrue(file_tree[0][0][0].name == 'test.py')
        self.assertTrue(file_tree[0][0][0].content is None)


class TestFileCreation(TestCase):
    """Tests that all required files are generated correctly."""
