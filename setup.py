from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

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
    install_requires=[
          'numpy',
          'pandas',
          'matplotlib',
          'scipy',
          'rspace_client'
      ])
