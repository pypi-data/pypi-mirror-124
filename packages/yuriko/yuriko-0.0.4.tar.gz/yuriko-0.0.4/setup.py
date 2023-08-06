"""
For testing:
python setup.py install

Upload to PyPI:
python setup.py bdist_wheel --universal
python setup.py sdist
twine upload dist/*
"""
import os
from setuptools import find_packages, setup


def read(file_name):
    try:
        return open(os.path.join(os.path.dirname(__file__), file_name)).read()
    except IOError:
        return ''


setup(
    name="yuriko",
    version='0.0.4',
    description="Encrypted notes",
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='encrypted, notes',
    author='Oleksandr Polieno',
    author_email='polyenoom@gmail.com',
    url="https://github.com/nanvel/yuriko",
    packages=find_packages(),
    install_requires=[
        'PyCryptodome'
    ],
    entry_points={
        'console_scripts': [
            'yuriko = yuriko.main:main'
        ]
    }
)
