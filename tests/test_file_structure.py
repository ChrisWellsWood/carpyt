"""Tests for creating file structure."""

import os
from pathlib import Path
import tempfile
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

    def test_simple_project(self):
        """Tests the file structure of the standard python template."""
        with tempfile.TemporaryDirectory() as tempdir:
            td_path = Path(tempdir)
            template_path = carpyt.TEMPLATES / 'python_module.yml'
            file_tree = carpyt.run_template_parser(template_path)
            file_tree.make(td_path)
            top_dir = td_path / 'python_module'
            self.assertTrue(top_dir.exists())
            lib_dir = top_dir / '{module}'
            self.assertTrue((lib_dir).exists())
            self.assertTrue((lib_dir / '__init__.py').exists())
            self.assertTrue((lib_dir / 'lib.py').exists())
            tests_dir = top_dir / 'tests'
            self.assertTrue(tests_dir.exists())
            self.assertTrue((tests_dir / 'test_lib.py').exists())
            docs_dir = top_dir / 'docs'
            self.assertTrue(docs_dir.exists())
            self.assertTrue((top_dir / 'README.md').exists())
            self.assertTrue((top_dir / 'MANIFEST.in').exists())
            self.assertTrue((top_dir / 'setup.py').exists())
