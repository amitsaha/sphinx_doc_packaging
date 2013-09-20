from __future__ import unicode_literals
import unittest
import os
import io
from string import Template
from sphinx2rpm import Spec, Archive

class TestSphinx2Rpm(unittest.TestCase):

    def setUp(self):
        self.config={}
        self.config['project'] = 'myproject'
        self.config['version'] = '1'
        self.config['release'] = '0'

    def test_genspec(self):

        spec = Spec()
        spec.genspec(self.config)

        with open('template.spec') as f:
            spec_template = Template(f.read())

        self.assertEquals(spec.spec_file, spec_template.safe_substitute
                          (project_name = self.config['project'],
                           project_version = self.config['version'],
                           project_release = self.config['release']))

    def test_writespec(self):
        #XXX: look into mock
        spec = Spec()
        spec.genspec(self.config)
        f = io.StringIO()
        spec.writespec(f)
        self.assertEquals(spec.spec_file, f.getvalue())

    def test_gen_tgz_info(self):

        archive = Archive()
        archive.gen_tgz_info(self.config)
        self.assertEquals(archive.tgz_file,'myproject-docs-1-0.tgz')
        self.assertEquals(archive.extract_dest, 'myproject-docs-1-0')
