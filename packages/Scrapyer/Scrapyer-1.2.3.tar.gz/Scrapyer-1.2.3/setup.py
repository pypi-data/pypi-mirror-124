# -*- coding: utf-8 -*-

# @Date    : 2021年10月26日
# @Author  : D.z.zhong
from os.path import dirname, join
from setuptools import setup, find_packages
from pkg_resources import parse_version
from setuptools import setup, find_packages, __version__ as setuptools_version
"""
打包的用的setup必须引入，
"""

VERSION = '1.2.3'

install_requires = [
    'Twisted>=17.9.0',
    'cryptography>=2.0',
    'cssselect>=0.9.1',
    'itemloaders>=1.0.1',
    'parsel>=1.5.0',
    'pyOpenSSL>=16.2.0',
    'queuelib>=1.4.2',
    'service_identity>=16.0.0',
    'w3lib>=1.17.0',
    'zope.interface>=4.1.3',
    'protego>=0.1.15',
    'itemadapter>=0.1.0',
    'setuptools',
    "oss2",
    "openpyxl",
    "PyPDF2",
    "pymysql",
    "pymongo",
    "redis",
    "pdfplumber",
    "python-magic-bin",
    "scrapy-redis",
    "PIL"
]
extras_require = {}
cpython_dependencies = [
    'lxml>=3.5.0',
    'PyDispatcher>=2.0.5',
]

def has_environment_marker_platform_impl_support():
    """Code extracted from 'pytest/setup.py'
    https://github.com/pytest-dev/pytest/blob/7538680c/setup.py#L31

    The first known release to support environment marker with range operators
    it is 18.5, see:
    https://setuptools.readthedocs.io/en/latest/history.html#id235
    """
    return parse_version(setuptools_version) >= parse_version('18.5')

if has_environment_marker_platform_impl_support():
    extras_require[':platform_python_implementation == "CPython"'] = cpython_dependencies
    extras_require[':platform_python_implementation == "PyPy"'] = [
        # Earlier lxml versions are affected by
        # https://foss.heptapod.net/pypy/pypy/-/issues/2498,
        # which was fixed in Cython 0.26, released on 2017-06-19, and used to
        # generate the C headers of lxml release tarballs published since then, the
        # first of which was:
        'lxml>=4.0.0',
        'PyPyDispatcher>=2.1.0',
    ]
else:
    install_requires.extend(cpython_dependencies)
setup(
    name='Scrapyer',
    version=VERSION,
    url='https://scrapy.org',
    project_urls={
        'Documentation': 'https://docs.scrapy.org/',
        'Source': 'https://github.com/Buliqioqiolibusdo/scrapyer',
        'Tracker': 'https://github.com/Buliqioqiolibusdo/scrapyer/issues',
    },
    description='A high-level Web Crawling and Web Scraping framework',
    # long_description=open('README.rst').read(),
    author='Buliqioqiolibusdo',
    maintainer='Buliqioqiolibusdo',
    maintainer_email='dingyeran@163.com',
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='scrapyer',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        'console_scripts': ['scrapyer = scrapy.cmdline:execute']
        },
      )