import pathlib
from setuptools import setup
from keyring import get_keyring
get_keyring()

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="psychopumpum",
    version="1.1.0",
    description="Read the latest Real Python tutorials",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/psychopumpum/psychopumpum-api",
    author="psychopumpum",
    author_email="fadhil@rhyn.tech",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=["psychopumpum"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "psychopumpum=__init__:main",
        ]
    },
)