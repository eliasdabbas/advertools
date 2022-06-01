#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

import os; os.listdir()
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "pandas>=1.1.0",
    "pyasn1>=0.4",
    "scrapy>=2.5.0",
    "twython>=3.8.0",
    "pyarrow>=5.0.0",
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
]

setup(
    author="Elias Dabbas",
    author_email='eliasdabbas@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Productivity and analysis tools for online marketing",
    entry_points={
        'console_scripts': [
            'advertools=advertools.cli:main',
            'adv=advertools.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='advertising marketing search-engine-optimization adwords '
             'seo sem bingads keyword-research',
    name='advertools',
    packages=find_packages(include=['advertools']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/eliasdabbas/advertools',
    version='0.13.1',
    zip_safe=False,
)
