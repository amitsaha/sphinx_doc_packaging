Packaging Sphinx docs as RPMs
-----------------------------

SPEC file templates
===================

Generic SPEC file to package a Sphinx doc directory as an RPM
package. The HTML files are installed in /usr/share/doc/<your-package-name>.

Files:

- sample_mydocs.spec
- sample_mydocs (sample Sphinx doc directory)

sphinx2rpm
==========

A script to  generate the SPEC file and create a .tgz of your docs
directory::

    $ ./sphinx2rpm.py
    Usage: sphinx2rpm.py docs_dir -p <project> -v <version> -r <release> [-o output_dir]

    Options:
      -h, --help            show this help message and exit
      -o OUTPUT_DIR, --output=OUTPUT_DIR
			    Output directory
      -p PROJECT, --project=PROJECT
			    Project name
      -v VERSION, --version=VERSION
			    Version
      -r RELEASE, --release=RELEASE
			    Release

Example
~~~~~~~

Here is an example to use sphinx2rpm.py from the git clone::


    $ ./sphinx2rpm.py ../sample_mydocs -p mydocs -v 1 -r 0
    Created files in /tmp/sphinx2rpm

In the /tmp/sphinx2rpm directory, the following files will be created::

    $ ls /tmp/sphinx2rpm/
    total 140
    -rw-rw-r-- 1 gene gene 67681 Sep 21 05:21 mydocs-docs-1-0.tgz
    -rw-rw-r-- 1 gene gene   923 Sep 21 05:21 mydocs_generated.spec


You can then use ``rpmbuild`` to build the RPM for the above::

    1. Place the .spec file in the SPECS/ directory
    2. Place the .tgz file in the SOURCES/ directory

Python versions and testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The above script should work with Python 2 and Python 3 both. There are some unit tests
in ``test_sphinx2rpm.py``.
