import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="kukiapipy",
    version="0.6",
    description="Unofficial API Library for Chatbot For Free",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["requests"],
    extras_require={
                      "dev":[
                          "pytest",
                      ],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itelai/kukiapipy",
    author="Moezilla",
    author_email="Pranavajay594@gmail.com"

)
