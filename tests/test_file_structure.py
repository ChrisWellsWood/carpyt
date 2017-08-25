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

    def test_branched_template(self):
        """Tests creation of branched parse tree."""
        template_path = TEST_TEMPLATES / 'nested_branched.yml'
        file_tree = carpyt.run_template_parser(template_path)
        self.assertTrue(file_tree.name == 'nested_branched')
        self.assertTrue(file_tree[0].name == 'docs')
        self.assertTrue(file_tree[1].name == 'tests')
        self.assertTrue(file_tree[1][0].name == 'test_files')
        self.assertTrue(file_tree[1][0].content is None)
        self.assertTrue(file_tree[2].name == '{module}')
        self.assertTrue(file_tree[2][0].name == '__init__.py')
        self.assertTrue('content' in file_tree[2][0].content)

    def test_linked_template(self):
        """Tests creation of parse tree with linked templates."""
        template_path = TEST_TEMPLATES / 'parent.yml'
        file_tree = carpyt.run_template_parser(template_path)
        self.assertTrue(file_tree.name == 'parent')
        self.assertTrue(file_tree[0].name == '{module}')
        self.assertTrue(file_tree[0][0].name == 'child')
        self.assertTrue(file_tree[0][0][0].name == 'test_files')
        self.assertTrue(file_tree[0][0][0][0].name == 'tests.py')
        self.assertTrue(file_tree[0][0][0][0].content is None)
        self.assertTrue(file_tree[1].name == 'setup.py')
        self.assertTrue(file_tree[1].content is None)

    def test_recursive_template(self):
        """Tests error handling in recursive linked templates."""
        template_path = TEST_TEMPLATES / 'recursive.yml'
        with self.assertRaises(RecursionError):
            carpyt.run_template_parser(template_path)

    def test_reuse_template(self):
        """Tests reuse of linked templates."""
        template_path = TEST_TEMPLATES / 'reuse.yml'
        file_tree = carpyt.run_template_parser(template_path)
        self.assertTrue(len(file_tree.content) == 1)


class TestFileCreation(TestCase):
    """Tests that all required files are generated correctly."""
