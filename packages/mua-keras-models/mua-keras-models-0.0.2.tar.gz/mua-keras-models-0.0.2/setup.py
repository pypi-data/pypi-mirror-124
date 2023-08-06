from setuptools import setup
from setuptools import find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="mua-keras-models",
    version="0.0.2",
    description="keras models, that I want to be wrapped around",
    long_description=long_description,
    long_description_content_type="text/markdown",  # This is important!
    url="https://github.com/maifeeulasad/mua-keras-models",
    author="Maifee Ul Asad",
    author_email="maifeeulasad@gmail.com",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],
)
