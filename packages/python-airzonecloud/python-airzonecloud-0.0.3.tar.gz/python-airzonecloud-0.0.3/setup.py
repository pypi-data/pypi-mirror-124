from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="python-airzonecloud",
    version="0.0.3",
    author="José Luis Maroto",
    author_email="maroto.joseluis@gmail.com",
    description="A package to connect to AirZone cloud",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jlmaroto/python-airzonecloud",
    packages=["airzonecloud"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
