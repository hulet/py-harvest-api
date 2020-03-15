from setuptools import setup
from harvest import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='harvest_api',
    author='Ramon Moraes',
    author_email='ramon@vyscond.io',
    version=__version__,
    description='Harvest API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/vyscond/py-harvest-api',
    license='MIT',
    packages=[
        'harvest',
    ],
    install_requires=[
        'requests>=2.19.1',
    ],
)
