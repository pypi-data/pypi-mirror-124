from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

version = "0.1"

setup(
    name="pak8",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
)
