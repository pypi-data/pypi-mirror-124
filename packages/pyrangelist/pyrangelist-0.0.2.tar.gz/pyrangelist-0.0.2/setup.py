import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrangelist",
    version="0.0.2",
    author="Sergiy Popovych",
    author_email="sergiy.popovich@gmail.com",
    description="Implementation of the RangeList datastructure in python. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={"": ["*.py"]},
    install_requires=["intervaltree"],
    entry_points={},
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
