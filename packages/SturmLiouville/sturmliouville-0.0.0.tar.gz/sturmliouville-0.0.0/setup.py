#  -*- coding: utf-8 -*-
"""

Author: Rafael R. L. Benevides
Date: 19/10/2021

"""

import sturmliouville

from distutils.core import setup

setup(
    name='sturmliouville',
    version=sturmliouville.__version__,
    packages=[
        'sturmliouville',
        # 'jangada._settings',
        # 'jangada.utils',
        # 'jangada.primitives',
        # 'jangada.plotting',
        # 'jangada.timeseries'
    ],
    # license='MIT',
    description='Sturm-Liouville Eigenvalues and Eigenfunctions Problem Solver',
    # author=jangada.__author__,
    # author_email="rafaeluz821@gmail.com",
    # url='',
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # 'Intended Audience :: Data Scientists',  # Define that your audience are developers
        # 'Topic :: Software Development :: Build Tools',
        # 'License :: OSI Approved :: MIT License',  # Again, pick a license
        # 'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
    ],
)