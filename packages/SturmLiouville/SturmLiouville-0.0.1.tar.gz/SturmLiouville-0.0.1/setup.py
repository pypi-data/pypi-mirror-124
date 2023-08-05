import sturmliouville

from setuptools import setup

setup(
    name='SturmLiouville',
    version=sturmliouville.__version__,
    packages=['sturmliouville'],
    url='https://github.com/RafaelLuz/SturmLiouville',
    license='MIT',
    author='Rafael R. L. Benevides',
    author_email='rafaeluz821@gmail.com',
    description='Sturm-Liouville Eigenvalue Problem Solver',
    long_description="Given a Sturm-Liouville Problem, this package calculates its eigenvalues, eigenfunctions and provides a series of related tools",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy'
    ],
    python_requires='>=3.9',
)
