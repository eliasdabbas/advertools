
from setuptools import setup, find_packages
from codecs import open
from os import path

setup(
    name='advertools',
    version='0.1.1',
    description='Productivity and analysis tools for online marketing',
    long_description='A set of tools that help online marketing people '
                     'create campaigns, manage them, analyze keywords,'
                     'and more. One of the main use cases is generating'
                     'combinations of keywords for setting up large search'
                     'campaigns, together with all the tasks that come with'
                     'setting up campaigns, ad groups, and ads.',
    url='https://github.com/eliasdabbas/advertools',
    author='Elias Dabbas',
    author_email='eliasdabbas@gmail.com',
    license='MIT',
    keywords='marketing advertising adwords analytics seo sem',
    install_requires=['pandas'],
    python_requires='>=3',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],

)
