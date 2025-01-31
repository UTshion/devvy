import click
from pathlib import Path
from .project_detector import ProjectDetector
from .environment_manager import EnvironmentManager


@click.command()
@click.argument("project_path", type=click.Path(exists=True), default=".")
def main(project_path: str):
    """Devvy(Development + savvy) CLI"""
    project_path = Path(project_path).resolve()
    detector = ProjectDetector(project_path)
    env_type = detector.detect()

    if env_type:
        manager = EnvironmentManager(project_path, env_type)
        manager.start_interactive()
    else:
        click.echo("No supported project type detected.")
