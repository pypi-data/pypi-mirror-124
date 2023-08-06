from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.6'
DESCRIPTION = 'Python Beckhoff communication over ads'
LONG_DESCRIPTION = 'A package that allows to read and write data between python script and Beckhoff PLC.'

# Setting up
setup(
    name="pycat3",
    version=VERSION,
    license='MIT',
    author="Sofian Hanash",
    author_email="soha@kea.dk",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pyads'],
    keywords=['python', 'beackhoff', 'ads'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
    ]
)