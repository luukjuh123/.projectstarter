import os
import shutil
import click
import subprocess

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")


@click.command()
@click.argument("project_name")
def cli(project_name):
    """
    This script initiates a new project with a set of predefined standards.
    """
    # Create a new project with Poetry
    subprocess.run(["poetry", "new", project_name], check=True)

    # Navigate to the project directory
    os.chdir(project_name)

    # Add dependencies
    subprocess.run(
        [
            "poetry",
            "add",
            "--dev",
            "mypy",
            "flake8",
            "flake8-annotations",
            "black",
            "pre-commit",
        ],
        check=True,
    )

    # Copy over template files
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith(".toml") or filename.endswith(".yaml"):
            shutil.copy(os.path.join(TEMPLATES_DIR, filename), ".")

    # Install pre-commit hooks
    subprocess.run(["poetry", "run", "pre-commit", "install"], check=True)

    click.echo(f"Project {project_name} has been created with predefined standards.")


if __name__ == "__main__":
    cli()
