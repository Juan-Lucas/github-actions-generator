"""
Unit tests for the WorkflowGenerator class.
"""

import pytest
import yaml
from pathlib import Path
from jinja2 import TemplateNotFound

from gha_generator.generator import WorkflowGenerator


class TestWorkflowGenerator:
    """Test suite for WorkflowGenerator class."""
    
    @pytest.fixture
    def generator(self):
        """Create a WorkflowGenerator instance for testing."""
        return WorkflowGenerator()
    
    @pytest.fixture
    def sample_variables(self):
        """Sample variables for template rendering."""
        return {
            "project_name": "test-project",
            "python_version": "3.11",
            "php_version": "8.2",
            "node_version": "18",
        }
    
    def test_generator_initialization(self, generator):
        """Test that generator initializes correctly."""
        assert generator is not None
        assert generator.templates_dir.exists()
        assert generator.env is not None
    
    def test_load_template_data_science(self, generator):
        """Test loading data-science template."""
        template = generator.load_template("data-science")
        assert template is not None
    
    def test_load_template_django(self, generator):
        """Test loading django-api template."""
        template = generator.load_template("django-api")
        assert template is not None
    
    def test_load_template_laravel(self, generator):
        """Test loading laravel-api template."""
        template = generator.load_template("laravel-api")
        assert template is not None
    
    def test_load_template_react(self, generator):
        """Test loading react-app template."""
        template = generator.load_template("react-app")
        assert template is not None
    
    def test_load_template_invalid(self, generator):
        """Test loading an invalid template raises ValueError."""
        with pytest.raises(ValueError, match="Template .* not found"):
            generator.load_template("non-existent-template")
    
    def test_render_template(self, generator, sample_variables):
        """Test rendering a template with variables."""
        template = generator.load_template("data-science")
        rendered = generator.render_template(template, sample_variables)
        
        assert rendered is not None
        assert "test-project" in rendered
        assert "3.11" in rendered
    
    def test_render_template_replaces_all_variables(self, generator, sample_variables):
        """Test that all Jinja2 variables are replaced."""
        template = generator.load_template("data-science")
        rendered = generator.render_template(template, sample_variables)
        
        # Check that no Jinja2 syntax remains
        assert "{{" not in rendered
        assert "}}" not in rendered
    
    def test_validate_output_valid_yaml(self, generator):
        """Test validating valid YAML content."""
        valid_yaml = """
        name: Test Workflow
        on: [push, pull_request]
        jobs:
          test:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
        """
        is_valid, message = generator.validate_output(valid_yaml)
        assert is_valid is True
        assert "valid" in message.lower()
    
    def test_validate_output_invalid_yaml(self, generator):
        """Test validating invalid YAML content."""
        invalid_yaml = """
        name: Test Workflow
        on: [push, pull_request
        jobs:
          test: invalid syntax here
        """
        is_valid, message = generator.validate_output(invalid_yaml)
        assert is_valid is False
        assert "invalid" in message.lower()
    
    def test_write_workflow(self, generator, tmp_path):
        """Test writing workflow content to file."""
        content = "name: Test\non: push\njobs:\n  test:\n    runs-on: ubuntu-latest"
        filename = "test-workflow.yml"
        
        workflow_file = generator.write_workflow(tmp_path, content, filename)
        
        assert workflow_file.exists()
        assert workflow_file.name == filename
        assert workflow_file.read_text() == content
    
    def test_write_workflow_creates_directory(self, generator, tmp_path):
        """Test that write_workflow creates output directory if needed."""
        nested_path = tmp_path / "nested" / "directory"
        content = "name: Test"
        filename = "workflow.yml"
        
        workflow_file = generator.write_workflow(nested_path, content, filename)
        
        assert workflow_file.exists()
        assert workflow_file.parent == nested_path
    
    def test_generate_complete_workflow(self, generator, sample_variables, tmp_path):
        """Test generating a complete workflow file."""
        workflow_file = generator.generate(
            "data-science",
            sample_variables,
            tmp_path,
            "ci.yml"
        )
        
        assert workflow_file.exists()
        assert workflow_file.name == "ci.yml"
        
        # Verify content is valid YAML
        content = workflow_file.read_text()
        parsed = yaml.safe_load(content)
        assert parsed is not None
        assert "name" in parsed
        assert "jobs" in parsed
    
    def test_generate_with_default_filename(self, generator, sample_variables, tmp_path):
        """Test generating workflow with default filename."""
        workflow_file = generator.generate(
            "data-science",
            sample_variables,
            tmp_path
        )
        
        assert workflow_file.exists()
        assert workflow_file.name == "ci.yml"
    
    def test_list_templates(self, generator):
        """Test listing all available templates."""
        templates = generator.list_templates()
        
        assert isinstance(templates, list)
        assert len(templates) > 0
        assert "data-science" in templates
        assert "django-api" in templates
        assert "laravel-api" in templates
        assert "react-app" in templates
        assert "base" not in templates  # base template should be excluded
    
    def test_list_templates_sorted(self, generator):
        """Test that templates are returned in sorted order."""
        templates = generator.list_templates()
        assert templates == sorted(templates)
    
    def test_generated_workflow_contains_project_name(self, generator, sample_variables, tmp_path):
        """Test that generated workflow contains the project name."""
        workflow_file = generator.generate(
            "data-science",
            sample_variables,
            tmp_path
        )
        
        content = workflow_file.read_text()
        assert sample_variables["project_name"] in content
    
    def test_generated_workflow_contains_python_version(self, generator, sample_variables, tmp_path):
        """Test that generated workflow contains the Python version."""
        workflow_file = generator.generate(
            "data-science",
            sample_variables,
            tmp_path
        )
        
        content = workflow_file.read_text()
        assert sample_variables["python_version"] in content
    
    def test_generate_django_workflow(self, generator, sample_variables, tmp_path):
        """Test generating Django API workflow."""
        workflow_file = generator.generate(
            "django-api",
            sample_variables,
            tmp_path,
            "django-ci.yml"
        )
        
        assert workflow_file.exists()
        content = workflow_file.read_text()
        assert "Django" in content or "django" in content
        assert "postgres" in content.lower()
    
    def test_generate_laravel_workflow(self, generator, sample_variables, tmp_path):
        """Test generating Laravel API workflow."""
        workflow_file = generator.generate(
            "laravel-api",
            sample_variables,
            tmp_path,
            "laravel-ci.yml"
        )
        
        assert workflow_file.exists()
        content = workflow_file.read_text()
        assert "Laravel" in content or "laravel" in content
        assert "composer" in content.lower()
    
    def test_generate_react_workflow(self, generator, sample_variables, tmp_path):
        """Test generating React app workflow."""
        workflow_file = generator.generate(
            "react-app",
            sample_variables,
            tmp_path,
            "react-ci.yml"
        )
        
        assert workflow_file.exists()
        content = workflow_file.read_text()
        assert "React" in content or "react" in content
        assert "npm" in content.lower()
