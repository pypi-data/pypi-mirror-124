from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='r_logger',
    version="0.1.1",
    packages=['r_logger'],
    author="Ramin Zarebidoky",
    author_email="ramin.zarebidoky@gmail.com",
    description="a customized way to use log",
    url="https://github.com/RaminZarebidoky/r_logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    python_requires=">=3.7"
)
