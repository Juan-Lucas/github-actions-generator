import click

try:
    import questionary
except ImportError:
    questionary = None

def interactive_mode():
    if questionary is None:
        click.echo("Le module 'questionary' n'est pas installé. Installez-le avec 'pip install questionary'.", err=True)
        return

    project_type = questionary.select(
        "Type de projet ?",
        choices=[
            "data-science",
            "django-api",
            "laravel-api",
            "react-app",
            "fastapi",
            "flask",
            "express",
            "vue",
            "docker"
        ]
    ).ask()
    project_name = questionary.text("Nom du projet ?").ask()
    python_version = questionary.text("Version Python ?", default="3.11").ask()
    php_version = questionary.text("Version PHP ?", default="8.2").ask()
    node_version = questionary.text("Version Node.js ?", default="18").ask()
    output = questionary.text("Répertoire de sortie ?", default=".github/workflows").ask()

    return {
        "project_type": project_type,
        "project_name": project_name,
        "python_version": python_version,
        "php_version": php_version,
        "node_version": node_version,
        "output": output
    }
