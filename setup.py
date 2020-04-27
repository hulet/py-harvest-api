from setuptools import setup
from harvest import __version__
from harvest import __name__
from harvest import __author__
from harvest import __author_email__


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name=__name__,
    author=__author__,
    author_email=__author_email__,
    version=__version__,
    description='Harvest API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/velvetkeyboard/py-harvest-api',
    license='MIT',
    packages=[
        'harvest',
    ],
    install_requires=[
        'requests>=2.19.1',
    ],
)
