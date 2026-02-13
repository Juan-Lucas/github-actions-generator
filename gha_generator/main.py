@cli.group()
def secrets():
    """Outils pour la gestion et la détection des secrets dans les workflows."""
    pass

@secrets.command()
@click.option("--file", "workflow_file", required=True, type=click.Path(exists=True), help="Fichier workflow YAML à scanner")
def scan(workflow_file):
    """Détecte les secrets potentiellement hardcodés dans un workflow GitHub Actions."""
    import re
    import yaml
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
@cli.command()
@click.option("--requirements", "req_file", default="requirements.txt", help="Fichier requirements à scanner (défaut: requirements.txt)")
def scan(req_file):
    """Scanne les dépendances Python avec safety et suggère les bonnes pratiques de sécurité GitHub Actions."""
    from rich.console import Console
    import subprocess
    import sys
    console = Console()
    try:
        console.print(f"Scan de sécurité des dépendances ({req_file})...")
        result = subprocess.run([
            sys.executable, "-m", "safety", "check", "--file", req_file, "--full-report"
        ], capture_output=True, text=True)
        if result.returncode == 0:
            console.print("[green]Aucune vulnérabilité critique détectée dans les dépendances.")
        else:
            console.print("[red]Vulnérabilités détectées :")
            console.print(result.stdout)
        # Conseils de sécurité pour GitHub Actions
        console.print("\nConseils GitHub Actions :")
        console.print("- Utilisez des versions fixes pour les actions (ex: actions/checkout@v4)")
        console.print("- Définissez explicitement les permissions dans vos jobs")
        console.print("- Ajoutez un timeout-minutes à chaque job")
        console.print("- Ne stockez jamais de secrets en dur dans les workflows")
        console.print("- Utilisez le scan lint (gha-gen lint) pour détecter d'autres problèmes")
    except Exception as e:
        console.print(f"[red]Erreur lors du scan : {e}")
        sys.exit(1)
@cli.command()
def check_update():
    """Vérifie si une nouvelle version de gha-generator est disponible sur PyPI."""
    import requests
    from rich.console import Console
    import sys
    try:
        pkg = "gha-generator"
        url = f"https://pypi.org/pypi/{pkg}/json"
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            Console().print(f"[yellow]Impossible de vérifier la version sur PyPI (erreur HTTP {r.status_code})")
            sys.exit(1)
        latest = r.json()["info"]["version"]
        from . import __version__
        current = __version__
        if current == latest:
            Console().print(f"[green]Vous utilisez la dernière version : {current}")
        else:
            Console().print(f"[bold yellow]Nouvelle version disponible : {latest} (vous avez {current})")
            Console().print(f"[cyan]Mettez à jour avec : pip install -U gha-generator")
    except Exception as e:
        Console().print(f"[red]Erreur lors de la vérification : {e}")
        sys.exit(1)
@cli.command()
@click.option(
    "--name",
    "-n",
    "project_name",
    required=True,
    help="Nom du projet à initialiser",
)
def init_project(project_name):
    """Crée la structure complète d'un projet (src/, tests/, .github/workflows, README)."""
    import os
    try:
        base = Path(project_name)
        (base / "src").mkdir(parents=True, exist_ok=True)
        (base / "tests").mkdir(parents=True, exist_ok=True)
        (base / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
        readme = base / "README.md"
        if not readme.exists():
            readme.write_text(f"# {project_name}\n\nProjet initialisé avec gha-gen init-project\n")
        click.echo(f"Structure du projet '{project_name}' créée :")
        click.echo(f"- {base}/src/")
        click.echo(f"- {base}/tests/")
        click.echo(f"- {base}/.github/workflows/")
        click.echo(f"- {base}/README.md")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
@cli.command()
@click.option(
    "--file",
    "-f",
    "workflow_file",
    required=True,
    type=click.Path(exists=True),
    help="Fichier workflow YAML à mettre à jour",
)
@click.option(
    "--type",
    "-t",
    "project_type",
    required=False,
    help="Type de template (pour forcer la mise à jour)",
)
@click.option(
    "--name",
    "-n",
    "project_name",
    required=False,
    help="Nom du projet (pour forcer la mise à jour)",
)
@click.option(
    "--python-version",
    default=None,
    help="Version Python (pour forcer la mise à jour)",
)
@click.option(
    "--php-version",
    default=None,
    help="Version PHP (pour forcer la mise à jour)",
)
@click.option(
    "--node-version",
    default=None,
    help="Version Node.js (pour forcer la mise à jour)",
)
def update(workflow_file, project_type, project_name, python_version, php_version, node_version):
    """Met à jour un workflow existant en régénérant le YAML (conserve le nom du fichier)."""
    import yaml
    try:
        with open(workflow_file, encoding="utf-8") as f:
            content = yaml.safe_load(f)
        # Déduire le type de template depuis le nom ou le contenu
        detected_type = project_type
        if not detected_type:
            name = content.get("name", "").lower()
            for tpl in ["data-science", "django-api", "laravel-api", "react-app", "fastapi", "flask", "express", "vue", "docker"]:
                if tpl in name:
                    detected_type = tpl
                    break
        if not detected_type:
            click.echo("Impossible de déterminer le type de template. Utilisez --type.", err=True)
            sys.exit(1)
        # Variables
        variables = {
            "project_name": project_name or content.get("env", {}).get("PROJECT_NAME") or content.get("name", "").split("-")[0].strip(),
            "python_version": python_version or content.get("env", {}).get("PYTHON_VERSION", "3.11"),
            "php_version": php_version or content.get("env", {}).get("PHP_VERSION", "8.2"),
            "node_version": node_version or content.get("env", {}).get("NODE_VERSION", "18"),
        }
        generator = WorkflowGenerator()
        new_content = generator.render_template(generator.load_template(detected_type), variables)
        with open(workflow_file, "w", encoding="utf-8") as f:
            f.write(new_content)
        click.echo(f"Workflow mis à jour : {workflow_file}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
@cli.command()
@click.option("--from", "from_file", required=True, type=click.Path(exists=True), help="Fichier workflow source (GitHub Actions)")
@click.option("--to", "to_ci", required=True, type=click.Choice(["gitlab-ci", "circleci"]), help="Plateforme cible (gitlab-ci, circleci)")
def export(from_file, to_ci):
    """Exporte un workflow GitHub Actions vers un autre format CI/CD (conversion basique)."""
    import yaml
    import sys
    from pathlib import Path
    try:
        with open(from_file, encoding="utf-8") as f:
            gha = yaml.safe_load(f)
        project_name = gha.get("name", "exported-workflow")
        jobs = gha.get("jobs", {})
        env = gha.get("env", {})
        # Conversion basique jobs/steps
        if to_ci == "gitlab-ci":
            gl = {}
            gl["stages"] = list(jobs.keys())
            for job_name, job in jobs.items():
                gl[job_name] = {}
                gl[job_name]["stage"] = job_name
                if "env" in job:
                    gl[job_name]["variables"] = job["env"]
                elif env:
                    gl[job_name]["variables"] = env
                steps = job.get("steps", [])
                script = []
                for step in steps:
                    if "run" in step:
                        script.append(step["run"])
                    elif "name" in step:
                        script.append(f"# {step['name']}")
                if script:
                    gl[job_name]["script"] = script
            out_file = Path(from_file).with_suffix(".gitlab-ci.yml")
            with open(out_file, "w", encoding="utf-8") as f:
                yaml.dump(gl, f, sort_keys=False, allow_unicode=True)
            click.echo(f"Exporté vers {out_file}")
        elif to_ci == "circleci":
            cc = {"version": 2.1, "jobs": {}, "workflows": {"version": 2, "gha-export": {"jobs": []}}}
            for job_name, job in jobs.items():
                cc["jobs"][job_name] = {"docker": [{"image": "cimg/python:3.11"}], "steps": []}
                steps = job.get("steps", [])
                for step in steps:
                    if "run" in step:
                        cc["jobs"][job_name]["steps"].append({"run": step["run"]})
                    elif "name" in step:
                        cc["jobs"][job_name]["steps"].append({"run": f"echo {step['name']}"})
                cc["workflows"]["gha-export"]["jobs"].append(job_name)
            out_file = Path(from_file).with_suffix(".circleci.yml")
            with open(out_file, "w", encoding="utf-8") as f:
                yaml.dump(cc, f, sort_keys=False, allow_unicode=True)
            click.echo(f"Exporté vers {out_file}")
        else:
            click.echo("Plateforme cible non supportée.", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
@cli.command()
def stats():
    """Affiche les statistiques d'utilisation de gha-gen."""
    try:
        from .stats import load_stats
        stats = load_stats()
        click.echo(f"\nStatistiques gha-gen :")
        click.echo(f"- Workflows générés : {stats['total']}")
        if stats["templates"]:
            click.echo("- Utilisation par template :")
            for tpl, count in sorted(stats["templates"].items(), key=lambda x: -x[1]):
                click.echo(f"  • {tpl} : {count}")
        else:
            click.echo("- Aucun template utilisé pour l'instant.")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
@cli.group()
def config():
    """Configurer les options globales de gha-gen."""
    pass

@config.command()
@click.argument("key")
@click.argument("value")
def set(key, value):
    """Définit une option globale (ex: python_version 3.12)."""
    from .config import load_config, save_config
    config = load_config()
    config[key] = value
    save_config(config)
    click.echo(f"Option '{key}' enregistrée : {value}")

@config.command()
@click.argument("key")
def get(key):
    """Affiche la valeur d'une option globale."""
    from .config import load_config
    config = load_config()
    value = config.get(key)
    if value is not None:
        click.echo(f"{key} = {value}")
    else:
        click.echo(f"Option '{key}' non définie.")
@cli.command()
@click.argument("shell", required=False, type=click.Choice(["bash", "zsh"]))
def completion(shell):
    """Génère le script d'auto-complétion pour bash ou zsh."""
    try:
        if not shell:
            click.echo("Précisez le shell : bash ou zsh (ex: gha-gen completion bash)")
            sys.exit(1)
        import subprocess
        prog = "gha-gen"
        if shell == "bash":
            out = subprocess.check_output([prog, "--help"], text=True)
            click.echo("# Ajoutez ceci à ~/.bash_completion ou sourcez-le dans ~/.bashrc")
            click.echo("_GHA_GEN_COMPLETE=source_bash {}".format(prog))
        elif shell == "zsh":
            click.echo("# Ajoutez ceci à ~/.zshrc ou sourcez-le dans votre session")
            click.echo("autoload -U compinit; compinit")
            click.echo("_GHA_GEN_COMPLETE=source_zsh {}".format(prog))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
@cli.command()
def init():
    """Mode interactif pour générer un workflow (questionnaire CLI)."""
    try:
        from .interactive import interactive_mode
        params = interactive_mode()
        if not params:
            sys.exit(1)
        click.echo(f"\nRésumé :")
        for k, v in params.items():
            click.echo(f"- {k}: {v}")
        confirm = click.confirm("Générer le workflow avec ces paramètres ?", default=True)
        if not confirm:
            click.echo("Annulé.")
            sys.exit(0)
        generator = WorkflowGenerator()
        output_path = Path(params["output"])
        create_directory_safe(output_path)
        workflow_file = generator.generate(
            params["project_type"],
            {
                "project_name": params["project_name"],
                "python_version": params["python_version"],
                "php_version": params["php_version"],
                "node_version": params["node_version"],
            },
            output_path
        )
        click.echo(f"Workflow créé : {workflow_file}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
@cli.command()
@click.option(
    "--file",
    "-f",
    "workflow_file",
    required=True,
    type=click.Path(exists=True),
    help="Path to the workflow file to lint (best practices)",
)
def lint(workflow_file: str):
    """Lint a GitHub Actions workflow file (best practices)."""
    try:
        from .validators import validate_strict
        file_path = Path(workflow_file)
        is_valid, issues = validate_strict(file_path)
        if is_valid:
            click.echo(f"Le workflow respecte les bonnes pratiques.")
        else:
            click.echo(f"Problèmes détectés :")
            for issue in issues:
                click.echo(f"- {issue}")
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)
"""
Main CLI entry point for GitHub Actions Generator.

This module provides the command-line interface for generating
GitHub Actions workflow files.
"""

import sys
from pathlib import Path

import click

from . import __version__
from .generator import WorkflowGenerator
from .utils import create_directory_safe


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
        "data-science",
        "django-api",
        "laravel-api",
        "react-app",
        "fastapi",
        "flask",
        "express",
        "vue",
        "docker"
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
@click.option(
    "--python-version",
    "-p",
    default=None,
    help="Python version (for Python projects)",
)
@click.option(
    "--php-version",
    default=None,
    help="PHP version (for PHP projects)",
)
@click.option(
    "--node-version",
    default=None,
    help="Node.js version (for Node projects)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=None,
    help="Output directory for the workflow file",
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    default=None,
    help="Fichier de configuration YAML (.gha-gen.yml)",
)
@click.option(
    "--env",
    multiple=True,
    default=None,
    help="Variables d'environnement personnalisées (clé=valeur, ex: --env FOO=bar)",
)
def create(
    project_type: str = None,
    project_name: str = None,
    python_version: str = None,
    php_version: str = None,
    node_version: str = None,
    output: str = None,
    config: str = None,
    workflows: str = None,
    env: tuple = None,
):
    """Create a new GitHub Actions workflow file. Supporte --workflows et --env pour générer plusieurs fichiers avec variables personnalisées."""
    import yaml
    from .utils import get_workflow_filename
    try:
        custom_env = {}
        if env:
            for item in env:
                # Supporte FOO=bar,FOO2=val2 ou --env FOO=bar --env BAR=val
                for pair in item.split(","):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        custom_env[k.strip()] = v.strip()

        if config:
            with open(config, encoding="utf-8") as f:
                conf = yaml.safe_load(f)
            project_type = conf.get("project", {}).get("type") or project_type
            project_name = conf.get("project", {}).get("name") or project_name
            python_version = conf.get("project", {}).get("python_version") or python_version or "3.11"
            php_version = conf.get("project", {}).get("php_version") or php_version or "8.2"
            node_version = conf.get("project", {}).get("node_version") or node_version or "18"
            output = conf.get("output") or output or ".github/workflows"
            if "workflows" in conf:
                workflows = conf["workflows"]
            if "env" in conf:
                for k, v in conf["env"].items():
                    custom_env[k] = v
        else:
            python_version = python_version or "3.11"
            php_version = php_version or "8.2"
            node_version = node_version or "18"
            output = output or ".github/workflows"

        if not project_type or not project_name:
            click.echo("❌ Spécifiez au minimum --type et --name ou fournissez un --config YAML valide.", err=True)
            sys.exit(1)

        output_path = Path(output)
        create_directory_safe(output_path)

        # Multi-workflows support
        workflow_list = []
        if workflows:
            if isinstance(workflows, str):
                workflow_list = [w.strip() for w in workflows.split(",") if w.strip()]
            elif isinstance(workflows, list):
                workflow_list = workflows
        else:
            workflow_list = ["ci"]

        from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
        generator = WorkflowGenerator()
        with Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            transient=True,
        ) as progress:
            task = progress.add_task("Génération des workflows...", total=len(workflow_list))
            for wf in workflow_list:
                variables = {
                    "project_name": project_name,
                    "python_version": python_version,
                    "php_version": php_version,
                    "node_version": node_version,
                    "workflow": wf,
                }
                if custom_env:
                    variables.update(custom_env)
                filename = get_workflow_filename(project_type, project_name)
                if wf != "ci":
                    filename = filename.replace("-ci.yml", f"-{wf}.yml")
                workflow_file = generator.generate(project_type, variables, output_path, filename=filename)
                try:
                    from .stats import increment_template
                    increment_template(project_type)
                except Exception:
                    pass
                progress.console.print(f"[green]Workflow '{wf}' créé : {workflow_file}")
                progress.update(task, advance=1)
        from rich.console import Console
        Console().print(f"[bold blue]Dossier de sortie : {output_path.absolute()}")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--type",
    "-t",
    "project_type",
    required=True,
    type=click.Choice([
        "data-science",
        "django-api",
        "laravel-api",
        "react-app",
        "fastapi",
        "flask",
        "express",
        "vue",
        "docker"
    ], case_sensitive=False),
    help="Type of project template to preview",
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
def preview(
    project_type: str,
    project_name: str,
    python_version: str,
    php_version: str,
    node_version: str,
):
    """Preview the generated workflow YAML without creating a file."""
    try:
        variables = {
            "project_name": project_name,
            "python_version": python_version,
            "php_version": php_version,
            "node_version": node_version,
        }
        generator = WorkflowGenerator()
        template = generator.load_template(project_type)
        content = generator.render_template(template, variables)
        click.echo("=" * 60)
        click.echo(content)
        click.echo("=" * 60)
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.group()
def template():
    """Gérer les templates personnalisés."""
    pass

@template.command()
@click.argument("name")
@click.option("--from", "from_file", type=click.Path(exists=True), required=False, help="Fichier YAML/Jinja à copier comme base")
def create(name, from_file):
    """Créer un nouveau template personnalisé (dans .gha-gen/templates)."""
    import shutil
    from pathlib import Path
    user_tpl_dir = Path.home() / ".gha-gen" / "templates"
    user_tpl_dir.mkdir(parents=True, exist_ok=True)
    dest = user_tpl_dir / f"{name}.yml"
    if dest.exists():
        click.echo(f"Le template '{name}' existe déjà dans {user_tpl_dir}", err=True)
        sys.exit(1)
    if from_file:
        shutil.copy(from_file, dest)
        click.echo(f"Template '{name}' créé à partir de {from_file} dans {dest}")
    else:
        dest.write_text("""# Nouveau template personnalisé\nname: {{ project_name }} - Custom Workflow\n# Ajoutez votre contenu ici\n""")
        click.echo(f"Template vierge '{name}' créé dans {dest}")

@template.command()
@click.argument("name")
def use(name):
    """Utiliser un template personnalisé (avec --type name dans create)."""
    user_tpl_dir = Path.home() / ".gha-gen" / "templates"
    tpl_path = user_tpl_dir / f"{name}.yml"
    if not tpl_path.exists():
        click.echo(f"Le template '{name}' n'existe pas dans {user_tpl_dir}", err=True)
        sys.exit(1)
    click.echo(f"Utilisez --type {name} avec gha-gen create pour générer un workflow depuis ce template.")

@cli.command()
def list_templates():
    """List all available project templates (y compris personnalisés, avec couleurs)."""
    try:
        from rich.console import Console
        from rich.table import Table
        generator = WorkflowGenerator()
        templates = generator.list_templates()
        # Ajoute les templates utilisateurs
        from pathlib import Path
        user_tpl_dir = Path.home() / ".gha-gen" / "templates"
        custom_tpls = []
        if user_tpl_dir.exists():
            for file in user_tpl_dir.glob("*.yml"):
                if file.stem not in templates:
                    custom_tpls.append(file.stem)
        # Descriptions (à enrichir si besoin)
        descriptions = {
            "data-science": "Data Science, ML, Jupyter Notebooks",
            "django-api": "Django REST Framework API",
            "laravel-api": "Laravel PHP API",
            "react-app": "React / Next.js Frontend",
            "fastapi": "FastAPI, Python async API",
            "flask": "Flask, API Python légère",
            "express": "Express.js, Node API",
            "vue": "Vue.js Frontend",
            "docker": "Build & Push Docker",
        }
        console = Console()
        table = Table(title="Templates disponibles", header_style="bold magenta")
        table.add_column("Nom", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Type", style="yellow")
        for tpl in sorted(templates):
            table.add_row(tpl, descriptions.get(tpl.replace(" (custom)", ""), "-"), "Officiel")
        for tpl in sorted(custom_tpls):
            table.add_row(tpl, "Template personnalisé", "Custom")
        console.print(table)
    except Exception as e:
        import click
        click.echo(f"Error: {str(e)}", err=True)
        import sys
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

        click.echo(f"Validating {workflow_file}...")

        file_path = Path(workflow_file)
        is_valid, message = validate_yaml(file_path)

        if is_valid:
            click.echo(f"{message}")
        else:
            click.echo(f"{message}", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == "__main__":
    main()
