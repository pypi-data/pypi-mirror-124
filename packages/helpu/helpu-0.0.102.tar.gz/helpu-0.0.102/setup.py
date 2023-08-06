"""
Date Created: 2021-10-17
Author: Noctsol
Summary:
    Config for releasing to pypi via GitHub Workflows
"""



# Default Py Packagaes
import re
import os
import subprocess
import setuptools



### THINGS YOU NEED TO FILL OUT - START

PROJECT_NAME = "helpu"  # What shows up on pypi and is used for pip install
AUTHOR = "Noctsol"              # Author of this project
EMAIL = "noctsol@pm.me"         # Your email address

# Quick description of your project
SHORT_DESCRIPT = "Class containing super convenience methods."

# URL of your project - usually github repo
PROJECT_URL = "https://github.com/Noctsol/lib-py-helpu"

### THINGS YOU NEED TO FILL OUT - END


# Gets the tag version numbers - for GitHub Workflows - Does not work locally
# Check is set to false because this will return nonzero status even though it works
git_tag_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE, check=False)
    .stdout.decode("utf-8")
    .strip()
)
print(f"--> Build #:{git_tag_version}")

# Checks that the tag version matches the format of 0[0][0].0[0][0].0[0][0]
pattern = re.compile("^\\d{1,3}.\\d{1,3}.\\d{1,3}$")
is_match = bool(pattern.match(git_tag_version))
assert is_match is True

# Reads the requirement.txt file in the root dir
folder_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(folder_path, "requirements.txt")
with open(file_path) as f:
    text = f.read()
packages_list = text.split("\n")

# Read the README file to get a long description for the package
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Mimic a setup cgf
setuptools.setup(
    name=PROJECT_NAME,
    version=git_tag_version,
    author=AUTHOR,
    author_email=EMAIL,
    description=SHORT_DESCRIPT,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=PROJECT_URL,
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'Topic :: Utilities'
    ],
    package_dir={"": "src"},
    packages=[PROJECT_NAME],
    python_requires=">=3.5",
    install_requires=packages_list
)
