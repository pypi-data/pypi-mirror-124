"""
    Installation script for LHAPDF management module
"""
from setuptools import setup, find_packages
import os


requirements = ["tqdm", "pyyaml", "numpy"]
PACKAGE = "lhapdf_management"
VERSION = "0.1"

this_directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(this_directory, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name=PACKAGE,
    version=VERSION,
    description="python-only lhapdf management",
    author="J.M.Cruz-Martinez",
    author_email="juan.cruz@lairen.eu",
    url="https://gitlab.com/hepcedar/lhapdf/-/merge_requests/12",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={
        "console_scripts": ["lhapdf_management = lhapdf_management.scripts.lhapdf_script:main"]
    },
    zip_safe=False,
    classifiers=[
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=requirements,
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
