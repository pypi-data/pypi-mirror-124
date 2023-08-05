import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.txt").read_text()

buf = (HERE / "cinirw/__init__.py").read_text()
loc1 = buf.find('__version__') + len('__version__')
loc2 = buf[loc1:].find("'") + 1
loc3 = buf[loc1+loc2:].find("'")
VERSION = buf[loc1+loc2:loc1+loc2+loc3]
print(VERSION)

setup(
    name="CINIRW",
    version=VERSION,
    author="Chaoqun Chen",
    author_email="chen.chaoqun.ext@99cloud.net",
    description="A INI Creator, Reader, Writer",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/chenchaotsun/scripts",
    license="GNU General Public License v3.0",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords='cinirw',
    packages=["cinirw"],
    install_requires=[],
    # package_dir={"ZPyPI": "src"},
    # packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
