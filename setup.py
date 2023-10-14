"""
Movie Recommender Setup Script

This script is used to package and distribute the Movie Recommender project.
It contains information about the project, including its name, version, authors,
description, and other relevant details, to facilitate distribution and installation.

For more information about the Movie Recommender project, visit:
https://github.com/git-ankit/MovieRecommender
"""

import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git-ankit",  # Replace with your own username
    version="1.0.0",
    author="Suraj,Amit,Jay,Ankit",
    author_email="tiwariankit1006@gmail.com",
    description="A recommendation engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/git-ankit/MovieRecommender",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
