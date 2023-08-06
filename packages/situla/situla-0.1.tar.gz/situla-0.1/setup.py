#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from glob import glob
from pathlib import Path, PurePath

from setuptools import find_packages, setup

from src import situla


def read(*names, **kwargs):
    with Path(PurePath.joinpath(Path(__file__).parent, *names)).open(
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='situla',
    version=situla.__version__,
    license='MIT',
    description='Create bins for features as part of a modeling pipeline.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Andy Reagan',
    author_email='andy@andyreagan.com',
    url='https://github.com/andyreagan/situla',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[PurePath(path).name.suffix[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/andyreagan/situla/issues',
    },
    keywords=[],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
    ],
    extras_require={},
    entry_points={},
)