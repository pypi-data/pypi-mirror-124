
import setuptools

from setuptools import setup, Extension
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'oi_trend',
    packages=setuptools.find_packages(),
    version = '0.0.2',
    include_package_data=True,
    description = 'Python library for OI trend',
    long_description=long_description,
    long_description_content_type="text/markdown",  author = 'VedantSonje',
    author_email = 'vedant.sonje12@gmail.com',
    url = '',
    install_requires=['pandas','scipy','nsepython'],
    keywords = [ 'python', 'trading', 'oi_trend'],
    classifiers=[
      'Intended Audience :: Developers',
      'Natural Language :: English',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: Implementation :: PyPy',
      'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)