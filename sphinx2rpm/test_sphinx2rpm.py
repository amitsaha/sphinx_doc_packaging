"""
Unit tests
"""

from __future__ import unicode_literals
import unittest
import io
from string import Template
from sphinx2rpm import Spec, Archive


class TestSphinx2Rpm(unittest.TestCase):

    def setUp(self):
        self.config = {}
        self.config['project'] = 'myproject'
        self.config['version'] = '1'
        self.config['release'] = '0'

    def test_genspec(self):

        """
        Test for generating spec file
        """

        spec = Spec()
        spec.genspec(self.config)

        with open('expected_spec.spec') as f:
            expected_specfile = f.read()

        self.assertEquals(spec.spec_file, expected_specfile)

    def test_writespec(self):
        """
        Test for writing a spec file
        """

        #XXX: look into mock
        spec = Spec()
        spec.genspec(self.config)
        f = io.StringIO()
        spec.writespec(f)
        self.assertEquals(spec.spec_file, f.getvalue())

    def test_gen_tgz_info(self):

        """
        test for the tgz info
        """

        archive = Archive()
        archive.gen_tgz_info(self.config)
        self.assertEquals(archive.tgz_file, 'myproject-docs-1-0.tgz')
        self.assertEquals(archive.extract_dest, 'myproject-docs-1-0')
