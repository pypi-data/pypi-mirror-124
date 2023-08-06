from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='wwshc',
    version='0.0.8',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='J0J0HA',
    package_dir={'': 'wwshc'},
    packages=find_packages(where='wwshc'),
    python_requires='>=3.7, <4'
)
