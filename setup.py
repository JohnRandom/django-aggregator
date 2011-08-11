import finddata
from setuptools import setup, find_packages
from dasdocc import build_version

setup(
    name="dasdocc",
    author="Moritz Krog",
    author_email="moritz@c-base.org",
    version=build_version(),
    packages=find_packages(),
    package_data=finddata.find_package_data(),
    include_package_data=True,
)