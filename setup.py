import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nneslib",
    version="0.1",
    author="Mingyi Liu",
    author_email="icecity96@outlook.com",
    description="nneslib is a Python library for evaluating nodes/edges importance in a graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="", #TODO: add github url
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)