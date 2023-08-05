from setuptools import find_packages
from setuptools import setup

meta = {
    "name": "jackhash",
    "description": "Japanese, ASCII, Chinese, Korean Hash encoding",
    "license": "MIT",
    "url": "https://github.com/amogorkon/jackhash",
    "version": "1.0.4",
    "author": "Anselm Kiefner",
    "author_email": "jackhash@anselm.kiefner.de",
    "python_requires": ">=3.6",
    "keywords": [
        "hash encoding unicode",
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
    ],
}


with open("README.md") as f:
    LONG_DESCRIPTION = f.read()

setup(
    packages=["jackhash"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    zip_safe=False,
    **meta
)
