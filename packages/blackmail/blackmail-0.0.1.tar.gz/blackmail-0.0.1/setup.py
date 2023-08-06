from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Blackmail'

setup(
    name='blackmail',
    version=VERSION,
    author='Varun Chopra',
    author_email='pypi@varunchopra.vc',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['email'],
)
