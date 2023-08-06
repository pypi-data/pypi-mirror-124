from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Helps you to scale,rotate and display text on the pygame window '
LONG_DESCRIPTION = 'A package that allows to scale,rotate and display text on the pygame window very quickly and easily '

# Setting up
setup(
    name="pygamehelper",
    version=VERSION,
    author="Asher Thomas Abraham",
    author_email="achutomonline@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pygame'],
    keywords=['python', 'text', 'rotate', 'pygame', 'scale'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)