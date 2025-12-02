"""
GitHub Actions Generator
========================

A CLI tool to generate customized GitHub Actions workflow files.

Author: GitHub Actions Generator Team
License: MIT
"""

__version__ = "0.1.0"
__author__ = "GitHub Actions Generator Team"
__license__ = "MIT"

from .generator import WorkflowGenerator
from .utils import (
    check_github_folder,
    create_directory_safe,
    get_template_path,
    validate_yaml,
)

__all__ = [
    "WorkflowGenerator",
    "check_github_folder",
    "create_directory_safe",
    "validate_yaml",
    "get_template_path",
]
