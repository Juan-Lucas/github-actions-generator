"""
Integration tests for the complete workflow generation process.
"""


import pytest
import yaml
from click.testing import CliRunner

from gha_generator.generator import WorkflowGenerator
from gha_generator.main import cli


class TestIntegration:
    """Integration test suite for complete workflow generation."""

    @pytest.fixture
    def runner(self):
        """Create a CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def generator(self):
        """Create a WorkflowGenerator instance."""
        return WorkflowGenerator()

    def test_end_to_end_data_science_workflow(self, runner, tmp_path):
        """Test complete data science workflow generation via CLI."""
        output_dir = tmp_path / ".github" / "workflows"

        result = runner.invoke(cli, [
            "create",
            "--type", "data-science",
            "--name", "ml-pipeline",
            "--python-version", "3.11",
            "--output", str(output_dir)
        ])

        # Check command succeeded
        assert result.exit_code == 0

        # Check file was created
        workflow_file = output_dir / "ci.yml"
        assert workflow_file.exists()

        # Check YAML is valid
        with open(workflow_file) as f:
            workflow_data = yaml.safe_load(f)

        assert workflow_data is not None
        assert "name" in workflow_data
        assert "ml-pipeline" in workflow_data["name"]
        assert "jobs" in workflow_data
        assert "test" in workflow_data["jobs"]

        # Check Python version is correct
        content = workflow_file.read_text()
        assert "3.11" in content

    def test_end_to_end_django_workflow(self, runner, tmp_path):
        """Test complete Django API workflow generation."""
        output_dir = tmp_path / "workflows"

        result = runner.invoke(cli, [
            "create",
            "--type", "django-api",
            "--name", "backend-api",
            "--python-version", "3.10",
            "--output", str(output_dir)
        ])

        assert result.exit_code == 0
        workflow_file = output_dir / "ci.yml"
        assert workflow_file.exists()

        with open(workflow_file) as f:
            yaml.safe_load(f)

        # Check for Django-specific elements
        content = workflow_file.read_text()
        assert "django" in content.lower() or "postgres" in content.lower()
        assert "migrate" in content.lower()
        assert "3.10" in content

    def test_end_to_end_laravel_workflow(self, runner, tmp_path):
        """Test complete Laravel API workflow generation."""
        output_dir = tmp_path / "workflows"

        result = runner.invoke(cli, [
            "create",
            "--type", "laravel-api",
            "--name", "laravel-backend",
            "--php-version", "8.2",
            "--output", str(output_dir)
        ])

        assert result.exit_code == 0
        workflow_file = output_dir / "ci.yml"
        assert workflow_file.exists()

        content = workflow_file.read_text()
        assert "laravel" in content.lower() or "php" in content.lower()
        assert "composer" in content.lower()
        assert "8.2" in content

    def test_end_to_end_react_workflow(self, runner, tmp_path):
        """Test complete React app workflow generation."""
        output_dir = tmp_path / "workflows"

        result = runner.invoke(cli, [
            "create",
            "--type", "react-app",
            "--name", "frontend-app",
            "--node-version", "18",
            "--output", str(output_dir)
        ])

        assert result.exit_code == 0
        workflow_file = output_dir / "ci.yml"
        assert workflow_file.exists()

        content = workflow_file.read_text()
        assert "react" in content.lower() or "node" in content.lower()
        assert "npm" in content.lower()
        assert "18" in content

    def test_workflow_yaml_structure(self, generator, tmp_path):
        """Test that generated workflow has correct YAML structure."""
        variables = {
            "project_name": "test-project",
            "python_version": "3.11",
            "php_version": "8.2",
            "node_version": "18",
        }

        workflow_file = generator.generate(
            "data-science",
            variables,
            tmp_path
        )

        with open(workflow_file) as f:
            workflow_data = yaml.safe_load(f)

        # Check required top-level keys
        assert "name" in workflow_data
        # Note: YAML parses "on:" as boolean True, not string "on"
        assert (True in workflow_data or "on" in workflow_data)
        assert "jobs" in workflow_data

        # Check jobs structure
        jobs = workflow_data["jobs"]
        assert len(jobs) > 0

        # Check at least one job has required fields
        first_job = list(jobs.values())[0]
        assert "runs-on" in first_job
        assert "steps" in first_job

    def test_no_jinja2_variables_in_output(self, generator, tmp_path):
        """Test that no Jinja2 template variables remain in output."""
        variables = {
            "project_name": "my-project",
            "python_version": "3.11",
            "php_version": "8.2",
            "node_version": "18",
        }

        templates = ["data-science", "django-api", "laravel-api", "react-app"]

        for template_type in templates:
            workflow_file = generator.generate(
                template_type,
                variables,
                tmp_path,
                f"{template_type}-ci.yml"
            )

            content = workflow_file.read_text()

            # Check no Jinja2 syntax remains
            assert "{{" not in content, f"Found '{{{{' in {template_type}"
            assert "}}" not in content, f"Found '}}}}' in {template_type}"
            assert "{%" not in content, f"Found '{{%' in {template_type}"
            assert "%}" not in content, f"Found '%}}' in {template_type}"

    def test_all_templates_generate_valid_yaml(self, generator, tmp_path):
        """Test that all templates generate valid YAML."""
        variables = {
            "project_name": "test-project",
            "python_version": "3.11",
            "php_version": "8.2",
            "node_version": "18",
        }

        templates = generator.list_templates()

        for template_type in templates:
            workflow_file = generator.generate(
                template_type,
                variables,
                tmp_path,
                f"{template_type}-test.yml"
            )

            # Should not raise exception
            with open(workflow_file) as f:
                workflow_data = yaml.safe_load(f)

            assert workflow_data is not None, f"Failed for {template_type}"

    def test_generated_workflow_contains_all_variables(self, generator, tmp_path):
        """Test that generated workflow contains all provided variables."""
        variables = {
            "project_name": "awesome-project",
            "python_version": "3.12",
            "php_version": "8.3",
            "node_version": "20",
        }

        # Test data-science template
        workflow_file = generator.generate(
            "data-science",
            variables,
            tmp_path
        )

        content = workflow_file.read_text()
        assert "awesome-project" in content
        assert "3.12" in content

    def test_multiple_workflows_in_same_directory(self, generator, tmp_path):
        """Test generating multiple workflows in the same directory."""
        variables = {
            "project_name": "multi-project",
            "python_version": "3.11",
            "php_version": "8.2",
            "node_version": "18",
        }

        # Generate multiple workflows
        workflow1 = generator.generate(
            "data-science",
            variables,
            tmp_path,
            "data-ci.yml"
        )

        workflow2 = generator.generate(
            "django-api",
            {**variables, "project_name": "django-project"},
            tmp_path,
            "django-ci.yml"
        )

        # Both should exist
        assert workflow1.exists()
        assert workflow2.exists()
        assert workflow1 != workflow2

    def test_validate_generated_workflow_via_cli(self, runner, tmp_path):
        """Test validating a generated workflow using the validate command."""
        # First, generate a workflow
        output_dir = tmp_path / "workflows"

        create_result = runner.invoke(cli, [
            "create",
            "--type", "data-science",
            "--name", "test-project",
            "--output", str(output_dir)
        ])

        assert create_result.exit_code == 0

        # Now validate it
        workflow_file = output_dir / "ci.yml"
        validate_result = runner.invoke(cli, [
            "validate",
            "--file", str(workflow_file)
        ])

        assert validate_result.exit_code == 0
        assert "valid" in validate_result.output.lower() or "✅" in validate_result.output

    def test_list_templates_shows_all_generated_templates(self, runner):
        """Test that list-templates shows all templates we can generate."""
        result = runner.invoke(cli, ["list-templates"])

        assert result.exit_code == 0

        expected_templates = ["data-science", "django-api", "laravel-api", "react-app"]
        for template in expected_templates:
            assert template in result.output
