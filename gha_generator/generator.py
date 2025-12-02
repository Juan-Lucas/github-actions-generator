"""
Workflow generator module.

This module contains the core logic for generating GitHub Actions
workflow files from templates.
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

from .utils import get_template_path, validate_yaml


class WorkflowGenerator:
    """Generator class for creating GitHub Actions workflows."""
    
    def __init__(self):
        """Initialize the workflow generator."""
        self.templates_dir = get_template_path()
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
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
            raise ValueError(
                f"Template '{template_type}' not found. "
                f"Available templates: {', '.join(self.list_templates())}"
            )
    
    def render_template(self, template: Template, variables: Dict[str, Any]) -> str:
        """
        Render a template with given variables.
        
        Args:
            template: Jinja2 Template object
            variables: Dictionary of variables to inject into template
            
        Returns:
            Rendered template as string
        """
        return template.render(**variables)
    
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
            return False, f"Invalid YAML syntax: {str(e)}"
    
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
        except IOError as e:
            raise IOError(f"Failed to write workflow file: {str(e)}")
    
    def generate(
        self,
        template_type: str,
        variables: Dict[str, Any],
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
            raise ValueError(f"Generated workflow is invalid: {message}")
        
        # Determine filename
        if filename is None:
            filename = "ci.yml"
        
        # Write to file
        workflow_file = self.write_workflow(output_path, content, filename)
        
        return workflow_file
    
    def list_templates(self) -> List[str]:
        """
        List all available templates.
        
        Returns:
            List of template names (without .yml extension)
        """
        templates = []
        
        if not self.templates_dir.exists():
            return templates
        
        for file in self.templates_dir.glob("*.yml"):
            if file.stem != "base":  # Exclude base template
                templates.append(file.stem)
        
        return sorted(templates)
