import codecs
import os
from setuptools import setup, find_packages
from commify.version import __version__

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

long_description = long_description.replace("[!NOTE]", "")
long_description = long_description.replace("[!Caution]", "")

setup(
    name='Commify',
    version=__version__,
    description='Commify: You Should Commit Yourself.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Matuco19',
    license="MATCO-Open-Source 1.0",
    url="https://matuco19.com/Commify",
    project_urls={
        'Source Code': 'https://github.com/Matuco19/Commify',  
        'Bug Tracker': 'https://github.com/Matuco19/Commify/issues', 
    },
    packages=find_packages(),
    install_requires=[
        'ollama',
        'GitPython',
        'g4f',
        'rich',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'commify=commify.main:main', 
        ],
    },
    keywords=[
        'python',
        'ai',
        'commit',
        'git',
        'github',
        'gpt',
        'language-model',
        'gpt-3',
        'gpt3',
        'commits',
        'gpt-4',
        'gpt4',
        'ollama',
        'ollama-api',
        'llama3',
        'llama3.1',
        'llama3.2',
        'llama3.3',
        'matuco19',
        'openai',
        'python3',
        'gitpython',
    ],
)
