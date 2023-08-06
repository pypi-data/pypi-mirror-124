from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.8'
DESCRIPTION = 'Module to upload data to database '
LONG_DESCRIPTION = 'A package that contains all the functions to upload the data '

# Setting up
setup(
    name="wenergiedatabasemodule",
    version=VERSION,
    author="Shinoj cm",
    author_email="amshinojcm@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['firebase_admin'],
    keywords=['python', 'energy', 'wenergie', 'batteryanalytics', 'database', 'database'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
