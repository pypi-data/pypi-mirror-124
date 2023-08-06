import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrangelist",
    version="0.1.2",
    author="Sergiy Popovych",
    author_email="sergiy.popovich@gmail.com",
    description="Implementation of the RangeList datastructure in python. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={"": ["*.py"]},
    install_requires=["intervaltree"],
    entry_points={},
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'astroid',
            'isort',
            'pylint',
            'black',
            'twine'
        ]
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
