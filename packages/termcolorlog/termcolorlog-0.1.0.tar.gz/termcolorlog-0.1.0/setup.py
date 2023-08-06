from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0'
DESCRIPTION = 'Colorize your terminal and log all your actions with colors'
LONG_DESCRIPTION = 'A package that allows to colorize your terminal and to log all your actions with colors.'

# Setting up
setup(
    name="termcolorlog",
    version=VERSION,
    author="DrMonocle",
    author_email="<contact.drmonocle@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'terminal', 'color', 'logging', 'color log', 'terminal log'],
    classifiers=[]
)