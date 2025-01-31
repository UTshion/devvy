# Devvy

An interactive development companion that provides language-specific commands and environment management from your terminal.

> The name "Devvy" combines "Development" and "savvy", reflecting its role as a knowledgeable assistant that helps developers navigate and manage their projects efficiently across different languages and frameworks.

# Installation

First, clone this repository and get into the directory.

```shell
git clone https://github.com/UTshion/devvy.git
cd devvy
```

## Using rye (Recommended)

```shell
rye sync
```

## Using pip

```shell
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS

# or
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## Using poetry

```shell
poetry install
```

## Using pipenv

```shell
pipenv install
```

# Usage

In devvy directory, just run Devvy as python module with specifying the target project's root directory.

```shell
python -m devvy path/to/project_root
```

Devvy automatically detects the project type based on configuration files and provides relevant commands through an interactive interface.

# Supported languages and frameworks

##  **Astro** (detected by `astro.config.mjs`)
  - Integration management
  - Development server
  - Build and check commands

## **Nix** (detected by `.nix` or `.flake` files)
  - Shell environment management
  - Flake operations
  - System rebuild support

## **Python** (detected by `pyproject.toml`)
  - Package management via Rye
  - Environment synchronization
  - Project initialization

## **Rust** (detected by `Cargo.toml`)
  - Dependency management
  - Build operations
  - Development workflow commands