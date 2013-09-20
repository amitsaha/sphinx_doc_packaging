#!/usr/bin/env python

'''
This script does two things:

1. Generates a best guess SPEC file generator for a RPM package
2. It also creates a .tgz of the docs directory
'''

from string import Template
import argparse
import os
import imp
import sys
import tarfile
from optparse import OptionParser

spec_template = Template('''
# Please replace the URL and the URL in Source0
# with correct project URLs
# and of course others
Name:           $project_name-docs
Version:        $project_version
Release:        $project_release
Summary:        Documentation and Samples for a project
License:        LGPLv2+
URL:            http://www.$project_name.org
Source0:        http://$project_name.org/%{name}-%{version}-%{release}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Group:          Documentation
BuildArch:      noarch
BuildRequires:  make
BuildRequires:  python-docutils
BuildRequires:  python-sphinx

%description
My docs packaged as an RPM

%prep
%setup -q -n %{name}-%{version}-%{release}

%build
make html

%install
mkdir -p %{buildroot}/%{_defaultdocdir}
cp -r %{_builddir}/%{name}-%{version}-%{release}/_build/html %{buildroot}/%{_defaultdocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_defaultdocdir}/%{name}
'''
)

def genspec(config, output):
    # write the spec file
    # use safe_substitute since we have $strings which are not
    # to be substituted
    spec_file= spec_template.safe_substitute(project_name=config.project,
                                             project_version=config.version,
                                             project_release=config.release)
    spec_file_name = '{0}_generated.spec'.format(config.project)
    with open(os.path.join(os.path.abspath(output),spec_file_name),'w') as f:
        f.write(spec_file)

    print 'Created SPEC file: {0}'.format(spec_file_name)

def gentgz(config, docs_dir, output):
    # create a tgz file from the supplied docs directory
    # The .tgz will extract to a directory such that it
    # matches the project name
    tgz_file = '{0}-docs-{1}-{2}.tgz'.format(config.project, config.version, config.release)
    extract_dest = '{0}-docs-{1}-{2}'.format(config.project, config.version, config.release)
    with tarfile.open(os.path.join(os.path.abspath(output), tgz_file), "w:gz") as tar:
        tar.add(docs_dir, arcname=extract_dest)
        print 'Created archive: {0}'.format(tgz_file)


def main(docs_dir, output):
    if not os.path.exists(os.path.abspath(output)):
        os.mkdir(output)

    # if the conf.py uses the modules which are hopefully
    # one level up
    orig = sys.path
    sys.path.append(os.path.split(docs_dir.rstrip('/'))[0])
    # load conf.py
    try:
        config = imp.load_source('conf.py',
                                 os.path.abspath('{0}/conf.py'.format(docs_dir)))
    except IOError: # file not found
        # try in docs_dir/src (SymPy for eg.)
        config = imp.load_source('conf.py',
                                 os.path.abspath('{0}/src/conf.py'.format(docs_dir)))

    genspec(config,output)
    gentgz(config, docs_dir, output)
    sys.path = orig

if __name__ == '__main__':
    usage = "usage: %prog docs_dir [-o output_dir]"
    parser = OptionParser(usage=usage)
    parser.add_option("-o", "--output", dest="output_dir",
                      default="output",
                      help="Ouptut directory")

    (options, args) = parser.parse_args()
    if not args:
        parser.print_help()
        sys.exit(1)

    main(args[0], options.output_dir)
