"""
Unit tests for the CLI interface.
"""

import pytest
from click.testing import CliRunner
from pathlib import Path

from gha_generator.main import cli, create, list_templates, validate


class TestCLI:
    """Test suite for CLI commands."""
    
    @pytest.fixture
    def runner(self):
        """Create a CLI test runner."""
        return CliRunner()
    
    def test_cli_help(self, runner):
        """Test that CLI help message is displayed."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "GitHub Actions Generator" in result.output
    
    def test_cli_version(self, runner):
        """Test that CLI version is displayed."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output
    
    def test_create_command_help(self, runner):
        """Test create command help."""
        result = runner.invoke(create, ["--help"])
        assert result.exit_code == 0
        assert "Create a new GitHub Actions workflow" in result.output
    
    def test_create_command_missing_required_args(self, runner):
        """Test create command without required arguments."""
        result = runner.invoke(create)
        assert result.exit_code != 0
    
    def test_create_command_with_valid_args(self, runner, tmp_path):
        """Test create command with valid arguments."""
        result = runner.invoke(create, [
            "--type", "data-science",
            "--name", "test-project",
            "--output", str(tmp_path)
        ])
        
        assert result.exit_code == 0
        assert "✅" in result.output or "created successfully" in result.output.lower()
        
        # Check that file was created
        workflow_file = tmp_path / "ci.yml"
        assert workflow_file.exists()
    
    def test_create_command_django_api(self, runner, tmp_path):
        """Test creating Django API workflow."""
        result = runner.invoke(create, [
            "--type", "django-api",
            "--name", "my-django-api",
            "--python-version", "3.11",
            "--output", str(tmp_path)
        ])
        
        assert result.exit_code == 0
        workflow_file = tmp_path / "ci.yml"
        assert workflow_file.exists()
        
        content = workflow_file.read_text()
        assert "my-django-api" in content
        assert "3.11" in content
    
    def test_create_command_laravel_api(self, runner, tmp_path):
        """Test creating Laravel API workflow."""
        result = runner.invoke(create, [
            "--type", "laravel-api",
            "--name", "my-laravel-api",
            "--php-version", "8.2",
            "--output", str(tmp_path)
        ])
        
        assert result.exit_code == 0
        workflow_file = tmp_path / "ci.yml"
        assert workflow_file.exists()
        
        content = workflow_file.read_text()
        assert "my-laravel-api" in content
        assert "8.2" in content
    
    def test_create_command_react_app(self, runner, tmp_path):
        """Test creating React app workflow."""
        result = runner.invoke(create, [
            "--type", "react-app",
            "--name", "my-react-app",
            "--node-version", "18",
            "--output", str(tmp_path)
        ])
        
        assert result.exit_code == 0
        workflow_file = tmp_path / "ci.yml"
        assert workflow_file.exists()
        
        content = workflow_file.read_text()
        assert "my-react-app" in content
        assert "18" in content
    
    def test_create_command_invalid_type(self, runner, tmp_path):
        """Test create command with invalid project type."""
        result = runner.invoke(create, [
            "--type", "invalid-type",
            "--name", "test-project",
            "--output", str(tmp_path)
        ])
        
        assert result.exit_code != 0
    
    def test_create_command_custom_python_version(self, runner, tmp_path):
        """Test create command with custom Python version."""
        result = runner.invoke(create, [
            "--type", "data-science",
            "--name", "ml-project",
            "--python-version", "3.10",
            "--output", str(tmp_path)
        ])
        
        assert result.exit_code == 0
        workflow_file = tmp_path / "ci.yml"
        content = workflow_file.read_text()
        assert "3.10" in content
    
    def test_list_templates_command(self, runner):
        """Test list-templates command."""
        result = runner.invoke(list_templates)
        
        assert result.exit_code == 0
        assert "data-science" in result.output
        assert "django-api" in result.output
        assert "laravel-api" in result.output
        assert "react-app" in result.output
    
    def test_list_templates_shows_all_templates(self, runner):
        """Test that list-templates shows all available templates."""
        result = runner.invoke(list_templates)
        
        assert result.exit_code == 0
        # Count the number of templates listed
        templates_count = result.output.count("•")
        assert templates_count >= 4  # At least 4 templates
    
    def test_validate_command_help(self, runner):
        """Test validate command help."""
        result = runner.invoke(validate, ["--help"])
        assert result.exit_code == 0
        assert "Validate a GitHub Actions workflow" in result.output
    
    def test_validate_command_valid_file(self, runner, tmp_path):
        """Test validate command with valid workflow file."""
        # Create a valid workflow file
        workflow_file = tmp_path / "test-workflow.yml"
        workflow_file.write_text("""
name: Test Workflow
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
""")
        
        result = runner.invoke(validate, ["--file", str(workflow_file)])
        assert result.exit_code == 0
        assert "✅" in result.output or "valid" in result.output.lower()
    
    def test_validate_command_invalid_file(self, runner, tmp_path):
        """Test validate command with invalid workflow file."""
        # Create an invalid workflow file
        workflow_file = tmp_path / "invalid-workflow.yml"
        workflow_file.write_text("""
name: Invalid Workflow
on: [push, pull_request
jobs:
  test: invalid syntax
""")
        
        result = runner.invoke(validate, ["--file", str(workflow_file)])
        assert result.exit_code != 0
        assert "❌" in result.output or "invalid" in result.output.lower()
    
    def test_validate_command_non_existent_file(self, runner, tmp_path):
        """Test validate command with non-existent file."""
        non_existent = tmp_path / "does-not-exist.yml"
        result = runner.invoke(validate, ["--file", str(non_existent)])
        assert result.exit_code != 0
    
    def test_create_creates_directory_if_not_exists(self, runner, tmp_path):
        """Test that create command creates output directory."""
        nested_dir = tmp_path / "nested" / "workflows"
        
        result = runner.invoke(create, [
            "--type", "data-science",
            "--name", "test-project",
            "--output", str(nested_dir)
        ])
        
        assert result.exit_code == 0
        assert nested_dir.exists()
        assert (nested_dir / "ci.yml").exists()
    
    def test_create_output_shows_file_location(self, runner, tmp_path):
        """Test that create command shows the file location in output."""
        result = runner.invoke(create, [
            "--type", "data-science",
            "--name", "test-project",
            "--output", str(tmp_path)
        ])
        
        assert result.exit_code == 0
        assert str(tmp_path) in result.output or "ci.yml" in result.output
