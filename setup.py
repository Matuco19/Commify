from setuptools import setup, find_packages

setup(
    name='Commify',
    version='1.0.0',
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
