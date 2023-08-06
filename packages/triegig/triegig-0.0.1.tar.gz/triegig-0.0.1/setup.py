from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='triegig',
    version = '0.0.1',
    description='User-Interactive Trie that allows users to add, remove, search, and emulate search prefix guess.',
    py_modules = ['tree', 'depth'],
    package_dir = {'': 'src'},
    long_description = long_description,
    long_description_content_type = "text/markdown",

)