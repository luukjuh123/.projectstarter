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
    subprocess.run(
        [
            "cookiecutter",
            "--no-input",
            TEMPLATES_DIR,
            f"project_name={project_name}",
        ],
        check=True,
    )

    os.chdir(project_name)

    subprocess.run(["poetry", "init", "--no-interaction"], check=True)

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
            "pytest",
            "pytest-cov",
            "sphinx",
            "pylint",
        ],
        check=True,
    )

    os.mkdir("docs")
    os.system("sphinx-quickstart docs --no-sep -q -p project_name -a author -v version")

    os.makedirs("tests")
    with open(os.path.join("tests", "__init__.py"), "w") as f:
        pass

    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith(".toml") or filename.endswith(".yaml"):
            shutil.copy(os.path.join(TEMPLATES_DIR, filename), ".")

    subprocess.run(["poetry", "run", "pre-commit", "install"], check=True)

    click.echo(f"Project {project_name} has been created with predefined standards.")


if __name__ == "__main__":
    cli()
