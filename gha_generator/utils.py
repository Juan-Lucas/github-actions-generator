"""
Utility functions for GitHub Actions Generator.

This module provides helper functions for file operations,
validation, and other common tasks.
"""

import os
import yaml
from pathlib import Path
from typing import Tuple, Optional


def get_template_path() -> Path:
    """
    Get the path to the templates directory.
    
    Returns:
        Path object pointing to templates directory
    """
    current_dir = Path(__file__).parent
    templates_dir = current_dir / "templates"
    return templates_dir


def check_github_folder(base_path: Path = None) -> Tuple[bool, str]:
    """
    Check if .github/workflows directory exists.
    
    Args:
        base_path: Base directory to check (defaults to current directory)
        
    Returns:
        Tuple of (exists: bool, path: str)
    """
    if base_path is None:
        base_path = Path.cwd()
    
    github_workflows = base_path / ".github" / "workflows"
    
    if github_workflows.exists():
        return True, str(github_workflows)
    else:
        return False, str(github_workflows)


def create_directory_safe(directory: Path) -> None:
    """
    Create directory safely with all parent directories.
    
    Args:
        directory: Path to directory to create
        
    Raises:
        OSError: If directory cannot be created
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create directory {directory}: {str(e)}")


def validate_yaml(file_path: Path) -> Tuple[bool, str]:
    """
    Validate YAML file syntax.
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    try:
        if not file_path.exists():
            return False, f"File not found: {file_path}"
        
        with open(file_path, "r", encoding="utf-8") as f:
            yaml.safe_load(f)
        
        return True, f"Valid YAML file: {file_path.name}"
        
    except yaml.YAMLError as e:
        return False, f"Invalid YAML syntax: {str(e)}"
    except Exception as e:
        return False, f"Error reading file: {str(e)}"


def handle_file_errors(func):
    """
    Decorator to handle common file operation errors.
    
    Args:
        func: Function to decorate
        
    Returns:
        Wrapped function with error handling
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {str(e)}")
        except PermissionError as e:
            raise PermissionError(f"Permission denied: {str(e)}")
        except IOError as e:
            raise IOError(f"I/O error: {str(e)}")
    
    return wrapper


def validate_project_name(name: str) -> Tuple[bool, str]:
    """
    Validate project name format.
    
    Args:
        name: Project name to validate
        
    Returns:
        Tuple of (is_valid: bool, message: str)
    """
    if not name:
        return False, "Project name cannot be empty"
    
    if len(name) < 2:
        return False, "Project name must be at least 2 characters long"
    
    # Check for invalid characters
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        if char in name:
            return False, f"Project name contains invalid character: {char}"
    
    return True, "Valid project name"


def get_workflow_filename(project_type: str, project_name: str = None) -> str:
    """
    Generate appropriate workflow filename.
    
    Args:
        project_type: Type of project template
        project_name: Optional project name
        
    Returns:
        Suggested filename for the workflow
    """
    if project_name:
        # Sanitize project name for filename
        safe_name = project_name.lower().replace(" ", "-")
        return f"{safe_name}-ci.yml"
    else:
        return f"{project_type}-ci.yml"


def read_yaml_file(file_path: Path) -> Optional[dict]:
    """
    Read and parse a YAML file.
    
    Args:
        file_path: Path to YAML file
        
    Returns:
        Parsed YAML content as dictionary, or None if error
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error reading YAML file: {str(e)}")
        return None


def write_yaml_file(file_path: Path, content: dict) -> bool:
    """
    Write dictionary to YAML file.
    
    Args:
        file_path: Path where to write the file
        content: Dictionary to write as YAML
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(content, f, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error writing YAML file: {str(e)}")
        return False
