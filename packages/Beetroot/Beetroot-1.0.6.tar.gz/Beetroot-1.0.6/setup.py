#Imports
import sys

#Python2 and Python1 are absolutely illegal
if not sys.version.startswith("3"):
    raise VersionError("Python version is not supported.")

import codecs
import os.path

from setuptools import setup
from pathlib import Path as p

#Exception classes
class VersionError(Exception):
    pass

class AuthorError(Exception):
    pass

def ga():
    with open(p("./beetroot/metadata.py"), "r", encoding="iso-8859-1") as f:
        code = f.read().split("\n")
        
        version = ""
        author = ""
        ae = ""
        
        done = []
        for item in code:
            if item.startswith("__author__"):
                yeet = item.split("\"")
                author = str(yeet[1])
                
            if item.startswith("__version__"):
                yeet = item.split("\"")
                version = str(yeet[1])
                
            if item.startswith("__authoremail__"):
                yeet = item.split("\"")
                ae = str(yeet[1])
            
        return [version, author, ae]

#Setting up...
setup(
    name="Beetroot",
    version=ga()[0],
    packages=[
        "beetroot"
    ],
    description="A General Purpose Utility package for Python 3",
    url="https://github.com/CuboidRaptor/Python-beetroot",
    author=ga()[1],
    author_email=ga()[2],
    license="GNU GPLv3",
    install_requires=[
    ],
    extras_require={
        "tts": [
            "pyttsx3>=2.90"
        ],
        "chatbot": [
            "chatterbot>=1.0.1",
            "spacy>=3.1.3",
            "pytz>=2021.3",
            "sqlalchemy>=1.2.19",
            "pymongo>=3.12.1"
        ],
        "all": [
            "pyttsx3>=2.90",
            "chatterbot>=1.0.1",
            "spacy>=3.1.3",
            "pytz>=2021.3",
            "sqlalchemy>=1.2.19",
            "pymongo>=3.12.1"
        ]
    }
)