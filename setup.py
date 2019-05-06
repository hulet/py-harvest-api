from setuptools import setup
from harvest import __version__

setup(
    name='harvest',
    author="Ramon Moraes",
    author_email="ramon@vyscond.io",
    version=__version__,
    description='Harvest API',
    long_description="".join(open("README.md")),
    url="https://github.com/vyscond/harvest",
    license="MIT",
    packages=[
        "harvest"
    ],
    install_requires=[
        'requests==2.19.1'
    ],
    # entry_points={
    #     "console_scripts": [
    #         "harvest=harvest.cli:main"
    #     ]
    # }
)

