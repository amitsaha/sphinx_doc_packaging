#!/usr/bin/env python

"""
This script does two things:

1. Generates a best guess SPEC file generator for the RPM package
2. It creates a .tgz of the docs directory supplied
"""
from __future__ import print_function, unicode_literals

import os
import sys
import tarfile
from optparse import OptionParser
from string import Template


class Spec:
    """
    A Spec file
    """
    def __init__(self, output_dir='/tmp/sphinx2rpm'):
        with open('template.spec') as f:
            self.spec_template = Template(f.read())
        self.output_dir = output_dir

    def genspec(self, config):
        self.spec_file = self.spec_template.substitute(
            project_name=config['project'],
            project_version=config['version'],
            project_release=config['release'])
        self.spec_file_name = '{0}_generated.spec'.format(config['project'])

    def writespec(self, fobj=None):
        # if a file object is passed in
        # use that, else create one
        # we don't close the file object if
        # we are passed one
        if not fobj:
            fobj = open(os.path.join(os.path.abspath(self.output_dir),
                                     self.spec_file_name), 'w')
            fobj.write(self.spec_file)
            fobj.close()
        else:
            fobj.write(self.spec_file)


class Archive:

    def gen_tgz_info(self, config):
        # create a tgz file from the supplied docs directory
        # The .tgz will extract to a directory such that it
        # matches the project name
        self.tgz_file = '{0}-docs-{1}-{2}.tgz'.format(config['project'],
                                                      config['version'],
                                                      config['release'])
        self.extract_dest = '{0}-docs-{1}-{2}'.format(config['project'],
                                                      config['version'],
                                                      config['release'])

    def write_tgz(self, docs_dir, output_dir='/tmp/sphinx2rpm'):
        with tarfile.open(os.path.join(os.path.abspath(output_dir),
                                       self.tgz_file), 'w:gz') as tar:
            tar.add(docs_dir, arcname=self.extract_dest)


def setup(args, options):

    docs_dir = args[0]
    # setup config dict
    config = {}
    # project name should be a single word
    # if the user spefices long project name, only
    # long will be taken
    config['project'] = options.project.split()[0]
    config['version'] = options.version
    config['release'] = options.release

    return docs_dir, config


def main(docs_dir, config, output_dir):

    if not os.path.exists(os.path.abspath(output_dir)):
        os.mkdir(output_dir)

    spec = Spec(output_dir)
    spec.genspec(config)
    spec.writespec()

    tar = Archive()
    tar.gen_tgz_info(config)
    tar.write_tgz(docs_dir, output_dir)


if __name__ == '__main__':
    usage = 'usage: %prog docs_dir -p '
    '<project> -v <version> -r <release> [-o output_dir]'

    parser = OptionParser(usage=usage)
    parser.add_option('-o', '--output', dest='output_dir',
                      default='/tmp/sphinx2rpm',
                      help='Output directory')
    parser.add_option('-p', '--project', dest='project',
                      help='Project name')
    parser.add_option('-v', '--version', dest='version',
                      help='Version')
    parser.add_option('-r', '--release', dest='release',
                      help='Release')

    (options, args) = parser.parse_args()

    # options check
    if not all([args, options.project, options.release, options.version]):
        parser.print_help()
        sys.exit(1)

    # setup_config
    docs_dir, config = setup(args, options)
    # start here
    main(docs_dir, config, options.output_dir)
    print('Created files in {0}'.format(options.output_dir))
