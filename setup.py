import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="script_utils",
    version="0.0.1",
    author="Achal Dave",
    author_email="achalddave@gmail.com",
    description="Simple utilities for python scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/achalddave/python-script-utils/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
