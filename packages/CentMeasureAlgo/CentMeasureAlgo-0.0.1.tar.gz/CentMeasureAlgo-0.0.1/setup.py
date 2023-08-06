from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

#with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Centrality Measure Algorithims'


# Setting up
setup(
    name="CentMeasureAlgo",
    version=VERSION,
    author="rahulleoak",
    author_email="<rahulleoak@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['networkx'],
    keywords=['python', 'personal', 'centrality measure'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)