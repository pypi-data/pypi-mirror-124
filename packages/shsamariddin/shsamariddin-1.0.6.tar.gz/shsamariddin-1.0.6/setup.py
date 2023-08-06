import pathlib

import matplotlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="shsamariddin",
    version="1.0.6",
    description="It squares the number",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/shsamariddin",
    author="Sharipov Samariddin",
    author_email="samariddin-sharipov-99@mail.ru",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["calc"],
    include_package_data=True,
    install_requires=["matplotlib"],
    entry_points={
        "console_scripts": [
            "calc=calc.__main__:main",
        ]
    },
)
