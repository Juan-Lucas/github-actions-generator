"""
Setup configuration for GitHub Actions Generator.
"""

from pathlib import Path

from setuptools import find_packages, setup

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
with open("requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Package metadata
setup(
    name="gha-generator",
    version="0.1.0",
    author="GitHub Actions Generator Team",
    author_email="",
    description="A CLI tool to generate customized GitHub Actions workflow files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/github-actions-generator",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/github-actions-generator/issues",
        "Source": "https://github.com/yourusername/github-actions-generator",
        "Documentation": "https://github.com/yourusername/github-actions-generator#readme",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    package_data={
        "gha_generator": [
            "templates/*.yml",
        ],
    },
    install_requires=requirements,
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "gha-gen=gha_generator.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    keywords="github-actions ci cd workflow automation devops",
    license="MIT",
    zip_safe=False,
)
