from setuptools import setup, find_packages

setup(
    name='Commify',
    version='1.0.1',
    description='Commify: You Should Commit Yourself.',
    long_description='Commify is a command-line interface (CLI) tool that generates meaningful, structured commit messages for Git repositories using AI. By analyzing the staged changes (diff) in your repository, it creates commit messages that follow conventional commit guidelines, optionally including emojis for better context and readability.',
    author='Matuco19',
    url="https://matuco19.com",
    packages=find_packages(),
    install_requires=[
        'ollama',
        'GitPython',
    ],
    entry_points={
        'console_scripts': [
            'Commify = commify.main:main', 
        ],
    },
)
