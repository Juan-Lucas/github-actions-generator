import re
import subprocess
import sys
from pathlib import Path

import click

from . import __version__
from .generator import WorkflowGenerator
from .utils import create_directory_safe, get_workflow_filename, validate_yaml


# 1. Définition du groupe principal en premier
@click.group()
@click.version_option(version=__version__, prog_name="gha-gen")
def cli():
    """GitHub Actions Generator - Generate customized CI/CD workflows."""
    pass

# 2. Commandes de gestion des secrets
@cli.group()
def secrets():
    """Outils pour la gestion et la détection des secrets dans les workflows."""
    pass

@secrets.command()
@click.option("--file", "workflow_file", required=True, type=click.Path(exists=True), help="Fichier workflow YAML à scanner")
def scan_secrets(workflow_file):
    """Détecte les secrets potentiellement hardcodés dans un workflow."""
    from rich.console import Console
    console = Console()
    patterns = [
        re.compile(r"(?i)(secret|token|password|key|api[_-]?key|auth)[^\n]*:[^\n]*['\"]?([A-Za-z0-9\-_=]{8,})['\"]?"),
        re.compile(r"(?i)(secret|token|password|key|api[_-]?key|auth)[^\n]*=[^\n]*['\"]?([A-Za-z0-9\-_=]{8,})['\"]?")
    ]
    with open(workflow_file, encoding="utf-8") as f:
        content = f.read()
    findings = []
    for pat in patterns:
        for m in pat.finditer(content):
            findings.append(m.group(0))
    if findings:
        console.print(f"[red]Secrets potentiellement hardcodés trouvés dans {workflow_file} :")
        for fnd in findings:
            console.print(f"  [yellow]- {fnd}")
        console.print("Corrigez ces valeurs en utilisant les secrets GitHub (ex: ${{ secrets.MA_VARIABLE }})")
    else:
        console.print(f"[green]Aucun secret hardcodé détecté dans {workflow_file}.")

# 3. Commande de statistiques
@cli.command()
def stats():
    """Affiche les statistiques d'utilisation de gha-gen."""
    try:
        from .stats import load_stats
        stats_data = load_stats()
        click.echo("\nStatistiques gha-gen :")
        click.echo(f"- Workflows générés : {stats_data['total']}")
        if stats_data["templates"]:
            click.echo("- Utilisation par template :")
            for tpl, count in sorted(stats_data["templates"].items(), key=lambda x: -x[1]):
                click.echo(f"  • {tpl} : {count}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

# 4. Configuration globale
@cli.group()
def config():
    """Configurer les options globales de gha-gen."""
    pass

@config.command()
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Définit une option globale."""
    from .config import load_config, save_config
    conf = load_config()
    conf[key] = value
    save_config(conf)
    click.echo(f"Option '{key}' enregistrée : {value}")

# 5. Création de workflow
@cli.command()
@click.option("--type", "-t", "project_type", required=False, type=click.Choice([
    "data-science", "django-api", "laravel-api", "react-app",
    "fastapi", "flask", "express", "vue", "docker"
], case_sensitive=False))
@click.option("--name", "-n", "project_name", required=False)
@click.option("--python-version", "-p", default=None)
@click.option("--php-version", default=None)
@click.option("--node-version", default=None)
@click.option("--output", "-o", type=click.Path(), default=None)
@click.option("--config", "config_file", type=click.Path(exists=True), default=None)
@click.option("--env", multiple=True, default=None)
def create(project_type, project_name, python_version, php_version, node_version, output, config_file, env):
    """Create a new GitHub Actions workflow file."""
    try:
        custom_env = {}
        if env:
            for item in env:
                for pair in item.split(","):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        custom_env[k.strip()] = v.strip()

        # Valeurs par défaut
        python_version = python_version or "3.11"
        php_version = php_version or "8.2"
        node_version = node_version or "18"
        output_dir = output or ".github/workflows"

        if not project_type or not project_name:
            click.echo("Spécifiez au minimum --type et --name.", err=True)
            sys.exit(1)

        output_path = Path(output_dir)
        create_directory_safe(output_path)

        generator = WorkflowGenerator()
        variables = {
            "project_name": project_name,
            "python_version": python_version,
            "php_version": php_version,
            "node_version": node_version,
            "workflow": "ci",
        }
        variables.update(custom_env)

        filename = get_workflow_filename(project_type, project_name)
        workflow_file = generator.generate(project_type, variables, output_path, filename=filename)
        click.echo(f"Workflow créé : {workflow_file}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

# 6. Mode interactif et autres outils
@cli.command()
def init():
    """Mode interactif pour générer un workflow."""
    from .interactive import interactive_mode
    params = interactive_mode()
    if params:
        # Logique de génération simplifiée ici...
        click.echo("Génération en cours...")

@cli.command()
@click.option("--requirements", "req_file", default="requirements.txt")
def scan_security(req_file):
    """Scanne les dépendances Python pour la sécurité."""
    from rich.console import Console
    console = Console()
    try:
        console.print(f"Scan de sécurité ({req_file})...")
        subprocess.run([sys.executable, "-m", "safety", "check", "--file", req_file], check=False)
    except Exception as e:
        console.print(f"[red]Erreur : {e}")

@cli.command()
@click.option("--file", "-f", "workflow_file", required=True, type=click.Path(exists=True))
def validate(workflow_file):
    """Valide un fichier workflow YAML."""
    is_valid, message = validate_yaml(Path(workflow_file))
    click.echo(message if is_valid else f"Erreur: {message}")

def main():
    cli()

if __name__ == "__main__":
    main()
