"""
Main CLI entry point for GitHub Actions Generator.

This module provides the command-line interface for generating
GitHub Actions workflow files.
"""

import sys
import click
from pathlib import Path
from typing import Optional

from . import __version__
from .generator import WorkflowGenerator
from .utils import check_github_folder, create_directory_safe


@click.group()
@click.version_option(version=__version__, prog_name="gha-gen")
def cli():
    """GitHub Actions Generator - Generate customized CI/CD workflows."""
    pass


@cli.command()
@click.option(
    "--type",
    "-t",
    "project_type",
    required=True,
    type=click.Choice(["data-science", "django-api", "laravel-api", "react-app"], case_sensitive=False),
    help="Type of project template to generate",
)
@click.option(
    "--name",
    "-n",
    "project_name",
    required=True,
    help="Name of the project",
)
@click.option(
    "--python-version",
    "-p",
    default="3.11",
    help="Python version (for Python projects)",
)
@click.option(
    "--php-version",
    default="8.2",
    help="PHP version (for PHP projects)",
)
@click.option(
    "--node-version",
    default="18",
    help="Node.js version (for Node projects)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=".github/workflows",
    help="Output directory for the workflow file",
)
def create(
    project_type: str,
    project_name: str,
    python_version: str,
    php_version: str,
    node_version: str,
    output: str,
):
    """Create a new GitHub Actions workflow file."""
    try:
        click.echo(f"🚀 Generating {project_type} workflow for '{project_name}'...")
        
        # Create output directory if it doesn't exist
        output_path = Path(output)
        create_directory_safe(output_path)
        
        # Prepare variables for template
        variables = {
            "project_name": project_name,
            "python_version": python_version,
            "php_version": php_version,
            "node_version": node_version,
        }
        
        # Generate workflow
        generator = WorkflowGenerator()
        workflow_file = generator.generate(project_type, variables, output_path)
        
        click.echo(f"✅ Workflow created successfully: {workflow_file}")
        click.echo(f"📝 File location: {workflow_file.absolute()}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def list_templates():
    """List all available project templates."""
    try:
        generator = WorkflowGenerator()
        templates = generator.list_templates()
        
        click.echo("📋 Available templates:")
        click.echo()
        for template in templates:
            click.echo(f"  • {template}")
        
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--file",
    "-f",
    "workflow_file",
    required=True,
    type=click.Path(exists=True),
    help="Path to the workflow file to validate",
)
def validate(workflow_file: str):
    """Validate a GitHub Actions workflow file."""
    try:
        from .utils import validate_yaml
        
        click.echo(f"🔍 Validating {workflow_file}...")
        
        file_path = Path(workflow_file)
        is_valid, message = validate_yaml(file_path)
        
        if is_valid:
            click.echo(f"✅ {message}")
        else:
            click.echo(f"❌ {message}", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
