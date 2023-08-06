from setuptools import setup
import re

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = ''
with open('menu/menu.py') as f:
    version = re.search(r'^version\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

packages = [
    'menu',
    'menu/classes',
    'menu/functions'
]

setup(
    name="menu.py",
    version=version,
    install_requires=[
        'keyboard'
    ],
    author="deadyeti",
    author_email="deadyeti@deadyeti.ca",
    description="A simple python package for in-terminal menu creation on Windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/readyyeti/menu.py",
    project_urls={
        "Bug Tracker": "https://github.com/readyyeti/menu.py/issues",
    },
    packages=packages,
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ]
)
