from os.path import abspath, dirname, join as pjoin
from setuptools import setup, find_packages
from injectorfount import __version__

root = dirname(abspath(__file__))


def execfile(fname, globs, locs=None):
    locs = locs or globs
    exec(compile(open(fname).read(), fname, "exec"), globs, locs)


version = __version__

with open('requirements.txt') as f:
    required = f.read().splitlines()
    required = [requirement for requirement in required if 'http' not in requirement]

with open('requirements-dev.txt') as f:
    required_ext = f.read().splitlines()
    required_ext = [requirement for requirement in required_ext if 'http' not in requirement]


setup(
    name="injectorfount",
    version=version,
    python_requires='>=3.6',
    description='',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers'
    ],
    packages=['injectorfount'],
    include_package_data=True,
    keywords=[
        'Injector',
        'Injector Provider'
        'Dependency Injection',
        'DI',
        'Dependency Injection framework',
        'Inversion of Control',
        'IoC',
        'Inversion of Control container',
    ],
    install_requires=required,
    license='MIT',
    extras_require={
        'test': required_ext
    }
)
