import setuptools
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def package_files(directory):
    """
    Recursively find all files in a (sub)directory.
    Source: https://stackoverflow.com/a/36693250
    """
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


install_requires = [
    "numpy>=1.16.4",
    "scipy>=1.4.1",
    "pandas>=0.24.2",
    "scikit-learn>=0.22.1",
    "tensorly==0.6.0",
    "OpenML>=0.9.0",
    "mkl>=1.0.0",
],
    

setuptools.setup(
    name="oboe",
    version="0.2.0",
    author="Chengrun Yang, Yuji Akimoto, Dae Won Kim, Madeleine Udell",
    author_email="cy438@cornell.edu",
    description="An AutoML pipeline selection system to quickly select a promising pipeline for a new dataset.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/udellgroup/oboe",
    project_urls={
        "Bug Tracker": "https://github.com/udellgroup/oboe/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude='large_files'),
    package_data={'': package_files('oboe/defaults')},
    install_requires=install_requires,
    python_requires=">=3.7",
)
