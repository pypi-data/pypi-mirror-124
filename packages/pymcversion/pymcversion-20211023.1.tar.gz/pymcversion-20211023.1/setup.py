from setuptools import setup, find_packages
import sys
from typing import (
    List,
)

from pymcversion import __VERSION__ as VERSION

install_requires: List[str] = [
    # dependencies like requirements.txt
    'requests', # https://pypi.org/project/requests/
    'pydantic', # https://pypi.org/project/pydantic/
]

python_version = sys.version_info

setup(
    name='pymcversion',
    version=VERSION, # '0.1.0-alpha', # == 0.1.0-alpha0 == 0.1.0a0

    # packages=[ 'PACKAGE_NAME', ],
    packages=find_packages(),
    include_package_data=True,

    entry_points = {
        'console_scripts': [
            # create `main` function in PACKAGE_NAME/scripts/my_command_module.py
            'mcversion = pymcversion.scripts.mcversion:main',
        ],
    },

    install_requires=install_requires,

    author='aoirint',
    author_email='aoirint@gmail.com',

    url='https://github.com/aoirint/pymcversion',
    description='Minecraft version info utility',

    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
