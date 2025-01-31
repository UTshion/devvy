import click
import os
from pathlib import Path
import subprocess
from typing import List, Tuple
from .project_detector import ProjectType
from rich.console import Console
from rich.theme import Theme


class EnvironmentManager:
    def __init__(self, project_path: Path, project_type: ProjectType):
        self.project_path = project_path
        self.project_type = project_type
        self.console = Console(theme=Theme({"warning": "red", "success": "green"}))
        self.original_cwd = (
            Path.cwd()
        )  # 現在の作業ディレクトリを保存(終了後にdevvyのディレクトリに戻るため)

    def start_interactive(self):
        """Start interactive command menu"""
        try:
            # 引数として与えられたプロジェクトのルートディレクトリに移動
            os.chdir(self.project_path)

            while True:
                self._show_menu()
                try:
                    choice = click.prompt(">", type=int)
                    if not self._handle_choice(choice):
                        break
                except (ValueError, click.Abort):
                    click.echo("Invalid input. Please try again.")
        finally:
            # 必ず元のディレクトリに戻る
            os.chdir(self.original_cwd)

    def _show_menu(self):
        """Display the appropriate menu based on project type"""
        click.clear()
        click.echo(click.style(f"[{self.project_type.name}]", reverse=True, bold=True))
        click.echo("")

        # initやnixos-rebuildの場合は、開発環境に影響を及ぼす重大な操作のため色を付ける
        options = self._get_menu_options()
        for i, (name, _) in enumerate(options, 1):
            if name.endswith("init") or name == "nixos-rebuild":
                self.console.print(f"[warning]{i}. [/warning][warning]{name}[/warning]")
            elif name == "exit":
                self.console.print(f"[success]{i}. [/success][success]{name}[/success]")
            else:
                click.echo(f"{i}. {name}")

        # 空行を追加して入力プロンプトを表示
        click.echo("")

    def _get_menu_options(self) -> List[Tuple[str, str]]:
        """Get menu options based on project type"""
        if self.project_type == ProjectType.PYTHON:
            return [
                ("rye add", "add"),
                ("rye remove", "remove"),
                ("rye sync", "sync"),
                ("rye init", "init"),
                ("exit", "exit"),
            ]
        elif self.project_type == ProjectType.RUST:
            return [
                ("cargo add", "add"),
                ("cargo remove", "remove"),
                ("cargo run", "run"),
                ("cargo check", "check"),
                ("cargo build", "build"),
                ("cargo init", "init"),
                ("exit", "exit"),
            ]
        elif self.project_type == ProjectType.ASTRO:
            return [
                ("astro add", "add"),
                ("astro dev", "dev"),
                ("astro check", "check"),
                ("astro build", "build"),
                ("exit", "exit"),
            ]
        elif self.project_type == ProjectType.NIX:
            return [
                ("nix shell", "shell"),
                ("nix develop", "develop"),
                ("nix build", "build"),
                ("nix run", "run"),
                ("nixos-rebuild", "rebuild"),
                ("exit", "exit"),
            ]
        return []

    def _handle_choice(self, choice: int) -> bool:
        """Handle menu choice and return whether to continue the loop"""
        options = self._get_menu_options()
        if 1 <= choice <= len(options):
            command_name, command_type = options[choice - 1]

            if command_name == "exit":
                return False

            # initタイプのコマンドは環境の初期化を行うため、慎重を期すため実行の最終確認を行う
            if command_type == "init":
                if (
                    click.prompt(
                        "Are you sure you want to run this command?(y/N)",
                        type=str,
                        default="N",
                    ).lower()
                    != "y"
                ):
                    return True

            if self.project_type == ProjectType.PYTHON:
                self._handle_python_command(command_type)
            elif self.project_type == ProjectType.RUST:
                self._handle_rust_command(command_type)
            elif self.project_type == ProjectType.ASTRO:
                self._handle_astro_command(command_type)
            elif self.project_type == ProjectType.NIX:
                self._handle_nix_command(command_type)

            input("\nPress Enter to continue...")
        return True

    def _handle_python_command(self, command_type: str):
        """Handle Python-specific commands"""
        if command_type == "add":
            self.console.print(f"[blink](rye: {command_type})[/blink] ", end="")
            packages = click.prompt("", type=str)
            subprocess.run(["rye", "add"] + packages.split())
        elif command_type == "remove":
            self.console.print(f"[blink](rye: {command_type})[/blink] ", end="")
            packages = click.prompt("", type=str)
            subprocess.run(["rye", "remove"] + packages.split())
        elif command_type == "sync":
            subprocess.run(["rye", "sync"])
        elif command_type == "init":
            subprocess.run(["rye", "init"])

    def _handle_rust_command(self, command_type: str):
        """Handle Rust-specific commands"""
        if command_type == "add":
            self.console.print(f"[blink](cargo: {command_type})[/blink] ", end="")
            crates = click.prompt("", type=str)
            for crate in crates.split():
                subprocess.run(["cargo", "add", crate])
        elif command_type == "remove":
            crates = click.prompt(f"(cargo: {command_type})", type=str)
            for crate in crates.split():
                subprocess.run(["cargo", "remove", crate])
        elif command_type == "run":
            subprocess.run(["cargo", "run"])
        elif command_type == "check":
            subprocess.run(["cargo", "check"])
        elif command_type == "build":
            if (
                click.prompt(
                    # リリースバージョンでビルドするか確認
                    "Do you build this project for release?(y/N)",
                    type=str,
                    default="N",
                ).lower()
                == "y"
            ):
                subprocess.run(["cargo", "build", "--release"])
            else:
                subprocess.run(["cargo", "build"])
        elif command_type == "init":
            subprocess.run(["cargo", "init"])

    def _handle_astro_command(self, command_type: str):
        """Handle Astro-specific commands"""
        if command_type == "add":
            self.console.print(f"[blink](astro: {command_type})[/blink] ", end="")
            integration = click.prompt("", type=str)
            subprocess.run(["bunx", "astro", "add", integration])
        elif command_type == "dev":
            subprocess.run(["bunx", "--bun", "astro", "dev"])
        elif command_type == "check":
            subprocess.run(["bunx", "--bun", "astro", "check"])
        elif command_type == "build":
            subprocess.run(["bunx", "--bun", "astro", "build"])

    def _handle_nix_command(self, command_type: str):
        """Handle Nix-specific commands"""
        if command_type == "shell":
            self.console.print(f"[blink](nix: {command_type})[/blink] ", end="")
            packages = click.prompt("", type=str, default="")
            cmd = ["nix", "shell"]
            if packages:
                cmd.extend(["-p"] + packages.split())
            subprocess.run(["alacritty", "-e"] + cmd)
        elif command_type == "develop":
            if not (self.project_path / "flake.nix").exists():
                click.echo("There is no flake environment.")
                return
            self.console.print(f"[blink](nix: {command_type})[/blink] ", end="")
            flake_args = click.prompt("", type=str, default="")
            cmd = ["nix", "develop"]
            if flake_args:
                cmd.append(flake_args)
            subprocess.run(cmd)
        elif command_type == "build":
            self.console.print(f"[blink](nix: {command_type})[/blink] ", end="")
            flake_url = click.prompt("", type=str)
            subprocess.run(["nix", "build", flake_url])
        elif command_type == "run":
            self.console.print(f"[blink](nix: {command_type})[/blink] ", end="")
            flake_url = click.prompt("", type=str)
            subprocess.run(["nix", "run", flake_url])
