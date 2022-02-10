from setuptools import setup
from os import path


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='adamacs',
    version='0.0.1',
    description='Architectures for Data Management and Computational Support.',
    long_description=readme,
    author='Daniel Müller-Komorowska',
    author_email='danielmuellermsc@gmail.com',
    url='https://github.com/SFB1089/adamacs.git',
    license=license,
    packages=['adamacs'],
    install_requires=requirements)
