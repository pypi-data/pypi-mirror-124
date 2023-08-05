import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as fh:
    readme = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-simple-access-key',
    version=os.getenv('PACKAGE_VERSION', '0.0.0').replace('refs/tags/', ''),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='A library that provides a simple token authorization for Django REST framework.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/anexia-it/drf-simple-access-key',
    author='Harald Nezbeda',
    author_email='HNezbeda@anexia-it.com',
    install_requires=[
        'django>=2.2',
        'djangorestframework>=3.10',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
