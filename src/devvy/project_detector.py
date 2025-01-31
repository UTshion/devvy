from pathlib import Path
from enum import Enum, auto
from typing import Optional


class ProjectType(Enum):
    PYTHON = auto()
    RUST = auto()
    ASTRO = auto()
    NIX = auto()


class ProjectDetector:
    def __init__(self, path: Path):
        self.path = path

    def detect(self) -> Optional[ProjectType]:
        """Detect project type based on files in directory"""
        if (self.path / "pyproject.toml").exists():
            return ProjectType.PYTHON
        elif (self.path / "Cargo.toml").exists():
            return ProjectType.RUST
        elif (self.path / "astro.config.mjs").exists():
            return ProjectType.ASTRO
        elif any(self.path.glob("*.nix")) or any(self.path.glob(".flake")):
            return ProjectType.NIX
        return None
