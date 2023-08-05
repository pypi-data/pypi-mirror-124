from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'File Handler'
LONG_DESCRIPTION = 'This is a package to perform simple and complex file handling operations.'

# Setting up
setup(
    name="full_file_handler",
    version=VERSION,
    author="Jenil Chudgar",
    author_email="jenilchudgarfamily@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['file','file handling','file io','easy file'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)