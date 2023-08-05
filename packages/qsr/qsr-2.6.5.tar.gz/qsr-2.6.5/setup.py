from setuptools import setup, find_packages
import codecs
import os

VERSION = '2.6.5'
DESCRIPTION = 'the simple screen record'

# Setting up
setup(
    name="qsr",
    version=VERSION,
    author="R-Stu-Softdev",
    author_email="r.studio.animation@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['screen-recorder-sdk'],
    keywords=['python', 'video', 'record', 'screen recorder', 'screen', 'rstuteam', 'simpleqsr'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
