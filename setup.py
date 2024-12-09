from setuptools import setup, find_packages
from commify.version import __version__
setup(
    name='Commify',
    version=__version__,
    description='Commify: You Should Commit Yourself.',
    long_description='Commify is a command-line interface (CLI) tool that generates meaningful, structured commit messages for Git repositories using AI. By analyzing the staged changes (diff) in your repository, it creates commit messages that follow conventional commit guidelines, optionally including emojis for better context and readability.',
    author='Matuco19',
    url="https://matuco19.com/Commify",
    packages=find_packages(),
    install_requires=[
        'ollama',
        'GitPython',
        'g4f',
    ],
    entry_points={
        'console_scripts': [
            'Commify = commify.main:main', 
        ],
    },
)
