from setuptools import find_packages, setup

setup(
    name="janggi",
    version="0.9.0",
    install_requires=["termcolor==1.1.0"],
    package_dir={"": "janggi"},
    packages=find_packages(where="janggi"),
)
