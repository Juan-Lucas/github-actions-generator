"""
Workflow generator module.

This module contains the core logic for generating GitHub Actions
workflow files from templates.
"""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

from .utils import get_template_path


class WorkflowGenerator:
    """Generator class for creating GitHub Actions workflows."""

    def __init__(self):
        """Initialize the workflow generator."""
        from pathlib import Path
        from jinja2 import ChoiceLoader
        self.templates_dir = get_template_path()
        user_tpl_dir = Path.home() / ".gha-gen" / "templates"
        loaders = [FileSystemLoader(str(self.templates_dir))]
        if user_tpl_dir.exists():
            loaders.insert(0, FileSystemLoader(str(user_tpl_dir)))
        self.env = Environment(
            loader=ChoiceLoader(loaders),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def load_template(self, template_type: str) -> Template:
        """
        Load a template by type.

        Args:
            template_type: Type of template (e.g., 'data-science', 'django-api')

        Returns:
            Jinja2 Template object

        Raises:
            TemplateNotFound: If template doesn't exist
            ValueError: If template type is invalid
        """
        template_file = f"{template_type}.yml"

        try:
            template = self.env.get_template(template_file)
            return template
        except TemplateNotFound:
            available = self.list_templates()
            suggestion = ''
            if available:
                suggestion = f"\nSuggestions : {', '.join(available)}"
            raise ValueError(
                f"Le template '{template_type}' est introuvable dans les templates disponibles.{suggestion}\n"
                f"Vérifiez l'orthographe ou utilisez 'gha-gen list-templates' pour la liste complète."
            ) from None

    def render_template(self, template: Template, variables: dict[str, Any]) -> str:
        """
        Render a template with given variables.

        Args:
            template: Jinja2 Template object
            variables: Dictionary of variables to inject into template

        Returns:
            Rendered template as string
        """
        try:
            return template.render(**variables)
        except Exception as e:
            raise ValueError(f"Erreur lors du rendu du template : {str(e)}\nVérifiez que toutes les variables nécessaires sont fournies.") from e

    def validate_output(self, content: str) -> tuple[bool, str]:
        """
        Validate the generated YAML content.

        Args:
            content: YAML content as string

        Returns:
            Tuple of (is_valid, message)
        """
        import yaml

        try:
            yaml.safe_load(content)
            return True, "YAML syntax is valid"
        except yaml.YAMLError as e:
            return False, f"YAML invalide : {str(e)}\nVérifiez la syntaxe générée ou utilisez un validateur YAML en ligne."

    def write_workflow(self, output_path: Path, content: str, filename: str) -> Path:
        """
        Write workflow content to file.

        Args:
            output_path: Directory path where to write the file
            content: Workflow content as string
            filename: Name of the output file

        Returns:
            Path to the created file

        Raises:
            IOError: If file cannot be written
        """
        output_path.mkdir(parents=True, exist_ok=True)

        workflow_file = output_path / filename

        try:
            with open(workflow_file, "w", encoding="utf-8") as f:
                f.write(content)
            return workflow_file
        except OSError as e:
            raise OSError(f"Impossible d'écrire le fichier workflow : {str(e)}\nVérifiez les permissions du dossier ou l'espace disque.") from e

    def generate(
        self,
        template_type: str,
        variables: dict[str, Any],
        output_path: Path,
        filename: str = None,
    ) -> Path:
        """
        Generate a complete workflow file.

        Args:
            template_type: Type of template to use
            variables: Variables to inject into template
            output_path: Directory where to save the workflow
            filename: Optional custom filename (default: ci.yml)

        Returns:
            Path to the generated workflow file

        Raises:
            ValueError: If template is invalid or variables are missing
            IOError: If file cannot be written
        """
        # Load template
        template = self.load_template(template_type)

        # Render template
        content = self.render_template(template, variables)

        # Validate output
        is_valid, message = self.validate_output(content)
        if not is_valid:
            raise ValueError(f"Le workflow généré est invalide : {message}\nCorrigez le template ou les variables d'entrée.")

        # Determine filename
        if filename is None:
            filename = "ci.yml"

        # Write to file
        workflow_file = self.write_workflow(output_path, content, filename)

        return workflow_file

    def list_templates(self) -> list[str]:
        """
        List all available templates (y compris personnalisés).

        Returns:
            List of template names (without .yml extension)
        """
        templates = []
        if self.templates_dir.exists():
            for file in self.templates_dir.glob("*.yml"):
                if file.stem != "base":
                    templates.append(file.stem)
        # Ajoute les templates utilisateurs
        from pathlib import Path
        user_tpl_dir = Path.home() / ".gha-gen" / "templates"
        if user_tpl_dir.exists():
            for file in user_tpl_dir.glob("*.yml"):
                if file.stem not in templates:
                    templates.append(file.stem)
        return sorted(templates)
