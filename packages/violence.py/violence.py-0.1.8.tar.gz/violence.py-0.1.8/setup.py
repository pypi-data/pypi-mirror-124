import os

from setuptools import setup


setup(
    name        = 'violence.py',
    version     = '0.1.8',
    description = '[SV] Violence',
    author      = 'Allan BlackWell',
    license     = 'AMB',
    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 5 - Production/Stable',

        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    platforms        = ['any'],
    packages         = [
        'violence', 
        'violence.utils', 
        'violence.ru'
    ],
    python_requires  = '>=3.6, <4',
    entry_points={
        'console_scripts': [
            'rupy=violence.ru.ru:__main__',
            'unrupy=violence.ru.ru:__unrupy__',
        ],
    },
)
