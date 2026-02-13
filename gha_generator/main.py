import sys
from pathlib import Path

import click

from . import __version__
from .generator import WorkflowGenerator
from .utils import create_directory_safe, get_workflow_filename, validate_yaml


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
    required=False,
    type=click.Choice([
        "data-science", "django-api", "laravel-api", "react-app",
        "fastapi", "flask", "express", "vue", "docker"
    ], case_sensitive=False),
    help="Type of project template to generate",
)
@click.option(
    "--name",
    "-n",
    "project_name",
    required=False,
    help="Name of the project",
)
@click.option("--python-version", "-p", default=None, help="Python version")
@click.option("--php-version", default=None, help="PHP version")
@click.option("--node-version", default=None, help="Node.js version")
@click.option("--output", "-o", type=click.Path(), default=None, help="Output directory")
@click.option("--config", type=click.Path(exists=True), default=None, help="YAML config file")
@click.option("--workflows", default=None, help="Comma-separated list of workflows")
@click.option("--env", multiple=True, default=None, help="Custom environment variables")
def create(
    project_type=None, project_name=None, python_version=None, php_version=None,
    node_version=None, output=None, config=None, workflows=None, env=None,
):
    """Create a new GitHub Actions workflow file."""
    import yaml
    try:
        custom_env = {}
        if env:
            for item in env:
                for pair in item.split(","):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        custom_env[k.strip()] = v.strip()

        if config:
            with open(config, encoding="utf-8") as f:
                conf = yaml.safe_load(f)
            project_type = conf.get("project", {}).get("type") or project_type
            project_name = conf.get("project", {}).get("name") or project_name
            python_version = conf.get("project", {}).get("python_version") or python_version
            output = conf.get("output") or output
            if "env" in conf:
                custom_env.update(conf["env"])

        # Fallback defaults
        python_version = python_version or "3.11"
        php_version = php_version or "8.2"
        node_version = node_version or "18"
        output_dir = output or ".github/workflows"

        if not project_type or not project_name:
            click.echo("Error: Please specify --type and --name or a valid --config.", err=True)
            sys.exit(1)

        output_path = Path(output_dir)
        create_directory_safe(output_path)

        workflow_list = [w.strip() for w in workflows.split(",")] if workflows else ["ci"]

        generator = WorkflowGenerator()
        for wf in workflow_list:
            variables = {
                "project_name": project_name,
                "python_version": python_version,
                "php_version": php_version,
                "node_version": node_version,
                "workflow": wf,
            }
            variables.update(custom_env)

            # Use ci.yml if wf is ci, otherwise use generator default
            filename = f"{wf}.yml" if workflows or wf == "ci" else get_workflow_filename(project_type, project_name)

            workflow_file = generator.generate(project_type, variables, output_path, filename=filename)
            click.echo(f"Workflow '{wf}' created successfully: {workflow_file}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command(name="list-templates")
def list_templates():
    """List all available project templates."""
    try:
        generator = WorkflowGenerator()
        templates = generator.list_templates()
        if not templates:
            click.echo("No templates found.")
            return

        click.echo("Available templates:")
        for tpl in sorted(templates):
            click.echo(f"• {tpl}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--file", "-f", "workflow_file", required=True, type=click.Path(exists=True))
def validate(workflow_file):
    """Validate a GitHub Actions workflow file."""
    try:
        is_valid, message = validate_yaml(Path(workflow_file))
        if is_valid:
            click.echo(f"Validation successful: {message}")
        else:
            click.echo(f"Validation failed: {message}", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()
