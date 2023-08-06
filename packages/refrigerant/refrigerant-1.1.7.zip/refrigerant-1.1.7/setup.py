#! /usr/bin/env python

import sys
from setuptools import setup
from bbfreeze import __version__


def main():
    install_requires = ["altgraph==0.9", "refrigerant-loader>=1.1.0,<1.2.0"]

    if sys.platform == 'win32':
        install_requires.append("pefile>=1.2.4")

    setup(name="refrigerant",
          version=__version__,
          entry_points={
             "console_scripts": ['bb-freeze = bbfreeze:main', 'bbfreeze = bbfreeze:main'],
             "distutils.commands": [
                 "bdist_bbfreeze = bbfreeze.bdist_bbfreeze:bdist_bbfreeze"]},
          install_requires=install_requires,
          packages=['bbfreeze', 'bbfreeze.modulegraph'],
          zip_safe=False,
          maintainer="Ross J. Duff",
          maintainer_email="rjdbcm@mail.umkc.edu",
          url="https://pypi.python.org/pypi/refrigerant/",
          description="create standalone executables from python scripts",
          platforms="Linux Windows",
          license="zlib/libpng license",
          classifiers=[
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: zlib/libpng License",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.4",
            "Programming Language :: Python :: 2.5",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Topic :: Software Development :: Build Tools",
            "Topic :: System :: Software Distribution"],
          long_description=open("README.rst").read())


if __name__ == '__main__':
    main()
