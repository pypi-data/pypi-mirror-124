import io
from pathlib import Path
"""
python -m pip install --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload dist/*
export CURL_CA_BUNDLE="" && python -m twine upload --repository-url https://nexus-ci.corp.dev.vtb/repository/puos-pypi-lib/ dist/*
"""
from setuptools import setup, find_packages

here = Path(__file__).parent

REQUIRED = ["orjson", "python-multipart"]

with io.open(here / 'README.md', encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(here / 'vtb_py_logging' / '__about__.py') as fp:
    exec(fp.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description='test',
    author=about['__author__'],
    author_email=about['__email__'],
    packages=find_packages(exclude=['tests']),
    install_requires=REQUIRED
)
