#!/usr/bin/env python3
"""
Setup script for Blender Add-on Development Template

This script automates the initial setup process for the development environment.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, cwd=None, shell=False):
    """Run a command and return True if successful"""
    try:
        result = subprocess.run(
            command if shell else command.split(),
            cwd=cwd,
            shell=shell,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Error running command: {command}")
        print(f"Exception: {e}")
        return False


def check_python():
    """Check if Python 3.10+ is available"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("Error: Python 3.10 or later is required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} found")
    return True


def create_venv():
    """Create Python virtual environment"""
    print("Creating Python virtual environment...")
    if run_command("python -m venv .venv"):
        print("✓ Virtual environment created successfully")
        return True
    else:
        print("✗ Failed to create virtual environment")
        return False


def get_venv_python():
    """Get the path to the Python executable in the virtual environment"""
    system = platform.system()
    if system == "Windows":
        return Path(".venv/Scripts/python.exe")
    else:
        return Path(".venv/bin/python")


def install_dependencies():
    """Install Python dependencies in the virtual environment"""
    print("Installing dependencies...")
    python_exe = get_venv_python()

    if not python_exe.exists():
        print("✗ Virtual environment Python not found")
        return False

    if run_command(f"{python_exe} -m pip install --upgrade pip"):
        print("✓ pip upgraded successfully")
    else:
        print("✗ Failed to upgrade pip")
        return False

    if run_command(f"{python_exe} -m pip install -r requirements.txt"):
        print("✓ Dependencies installed successfully")
        return True
    else:
        print("✗ Failed to install dependencies")
        return False


def update_settings_for_platform():
    """Update VS Code settings.json for the current platform"""
    print("Updating VS Code settings for current platform...")

    settings_path = Path(".vscode/settings.json")
    if not settings_path.exists():
        print("✗ VS Code settings.json not found")
        return False

    try:
        with open(settings_path, "r") as f:
            content = f.read()

        system = platform.system()
        if system in ["Darwin", "Linux"]:  # macOS or Linux
            # Comment out Windows paths and uncomment Unix paths
            content = content.replace(
                '"python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe", // Windows',
                '// "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe", // Windows',
            )
            content = content.replace(
                '// "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",     // macOS/Linux',
                '"python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",     // macOS/Linux',
            )
            content = content.replace(
                '"${workspaceFolder}/.venv/Lib/site-packages", // Windows path',
                '// "${workspaceFolder}/.venv/Lib/site-packages", // Windows path',
            )
            content = content.replace(
                '// "${workspaceFolder}/.venv/lib/python3.10/site-packages", // macOS/Linux path (adjust Python version if needed)',
                '"${workspaceFolder}/.venv/lib/python3.10/site-packages", // macOS/Linux path (adjust Python version if needed)',
            )
            content = content.replace(
                '"path": "${workspaceFolder}/.venv/Scripts/python.exe" // Windows',
                '// "path": "${workspaceFolder}/.venv/Scripts/python.exe" // Windows',
            )
            content = content.replace(
                '// "path": "${workspaceFolder}/.venv/bin/python"      // macOS/Linux',
                '"path": "${workspaceFolder}/.venv/bin/python"      // macOS/Linux',
            )

        with open(settings_path, "w") as f:
            f.write(content)

        print("✓ VS Code settings updated for current platform")
        return True

    except Exception as e:
        print(f"✗ Failed to update VS Code settings: {e}")
        return False


def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Install VS Code extensions:")
    print("   - Python (by Microsoft)")
    print("   - Blender Development (by Jacques Lucke)")
    print("\n2. Update Blender path in .vscode/settings.json:")
    print("   - Edit 'blender.blenderExecutable.path'")
    print("   - Set it to your Blender executable path")
    print("\n3. Open VS Code in this directory:")
    print("   code .")
    print("\n4. Start developing your Blender add-on!")
    print("   - Edit files in the 'addon/' directory")
    print("   - Use Ctrl+Shift+P -> 'Blender: Start' to launch Blender")
    print("   - Enable your add-on in Blender's preferences")


def main():
    """Main setup function"""
    print("Blender Add-on Development Template Setup")
    print("=" * 40)

    # Check Python version
    if not check_python():
        sys.exit(1)

    # Create virtual environment
    if not create_venv():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Update settings for platform
    if not update_settings_for_platform():
        sys.exit(1)

    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
