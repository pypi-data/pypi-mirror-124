import pathlib
from setuptools import setup, find_packages
import sys

# Python supported version checks
if sys.version_info[:2] < (3, 7):
    raise RuntimeError("Python version >= 3.7 required.")

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name = 'BSplineFit',
    version = '1.1.0',  # Ideally should be same as your GitHub release tag varsion
    description = 'A uniform cubic B-spline regression library',
    long_description=README,
    long_description_content_type="text/markdown",
    url = 'https://github.com/MarceloJacinto/BSplineFit',
    author = 'MarceloJacinto',
    author_email = 'marcelo.jacinto@tecnico.ulisboa.pt',
    license="MIT",
    classifiers = [],
    packages = find_packages(exclude=("tests",)),
    include_package_data=True,
    platforms = ["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    python_requires='>=3.8',
    install_requires=["numpy", "scipy", "sklearn"],
)