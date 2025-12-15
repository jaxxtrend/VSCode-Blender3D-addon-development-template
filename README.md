# VS Code Blender Add-on Development Template

A ready-to-use template repository for developing Blender 3D add-ons with VS Code, featuring Python virtual environments, autocomplete support, and integrated debugging.

## Features

- 🐍 **Python Virtual Environment** - Isolated dependency management with `venv`
- 🧠 **Autocomplete Support** - Full Blender API autocomplete via `fake-bpy-module`
- 🔧 **VS Code Integration** - Pre-configured workspace settings and debugging
- 🚀 **Hot Reload** - Automatic add-on reloading on file save
- 🐛 **Debugging** - Full debugging support with breakpoints
- 📁 **Clean Structure** - Organized project template with best practices

## Quick Start

1. **Use this template** by clicking "Use this template" on GitHub or clone it:
   ```bash
   git clone https://github.com/jaxxtrend/VSCode-Blender-addons-development-template.git my-blender-addon
   cd my-blender-addon
   ```

2. **Open in VS Code**:
   ```bash
   code .
   ```

3. **Follow the setup instructions below** to configure your development environment.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Visual Studio Code**: The code editor itself
- **Python 3.10+**: A standard Python installation on your system (separate from Blender's Python)
- **Blender 3.x+**: The Blender version you are developing for

## Setup Instructions

Follow these steps in order to configure your development environment.

### Step 1: Create and Activate a Python Virtual Environment

This isolates your project's Python dependencies.

1. **Open VS Code's Integrated Terminal**: Go to `Terminal > New Terminal` (or press `Ctrl+` or `Cmd+`)
2. **Create the `venv`**: In the terminal, run:
   ```bash
   python -m venv .venv
   ```
   This creates a `.venv` folder inside your project directory.
3. **Activate the `venv`**:
   - **Windows (PowerShell):**
     ```bash
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```bash
     .venv\Scripts\activate.bat
     ```
   - **macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```
   You should see `(.venv)` appear at the beginning of your terminal prompt.

### Step 2: Install Dependencies

With your `venv` active, install the required dependencies:

```bash
pip install -r requirements.txt
```

This installs `fake-bpy-module-latest` which provides Blender API autocomplete.

### Step 3: Install Essential VS Code Extensions

1. Go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X`)
2. Search for and install:
   - **Python** (by Microsoft)
   - **Blender Development** (by Jacques Lucke)

### Step 4: Configure Blender Path

Update the Blender executable path in `.vscode/settings.json`:

1. Open `.vscode/settings.json`
2. Update the `blender.blenderExecutable.path` setting with your Blender installation path:
   - **Windows**: `"C:/Program Files/Blender Foundation/Blender 4.2/blender.exe"`
   - **macOS**: `"/Applications/Blender.app/Contents/MacOS/Blender"`
   - **Linux**: `"/usr/bin/blender"` or path to your Blender binary

### Step 5: Configure Python Interpreter Path (if needed)

The template is pre-configured for most setups, but you may need to adjust paths in `.vscode/settings.json`:

- **Windows**: Paths are already configured for Windows
- **macOS/Linux**: Uncomment the macOS/Linux paths and comment out Windows paths

## Development Workflow

### Starting Development

1. **Start Blender from VS Code**:
   - Open the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
   - Search for "Blender: Start" and select it
   - Blender will launch with your add-on linked

2. **Activate Your Add-on in Blender**:
   - In Blender, go to `Edit > Preferences > Add-ons`
   - Search for "Template Add-on" and enable it

### Coding with Autocomplete

- Edit files in the `addon/` directory
- Enjoy full autocomplete for `bpy`, `mathutils`, and other Blender modules
- VS Code will show linting errors and warnings

### Hot Reload

- Simply save your Python files in VS Code
- Your add-on will automatically reload in the running Blender instance
- No need to manually reload or restart Blender

### Debugging

1. Set breakpoints by clicking in the gutter next to line numbers
2. Go to the Run and Debug view (`Ctrl+Shift+D`)
3. Select "Blender: Launch & Debug" configuration
4. Click the green "Start Debugging" play button
5. VS Code will pause at breakpoints when your code executes

## Project Structure

```
my-blender-addon/
├── .vscode/
│   ├── settings.json      # VS Code workspace settings
│   └── launch.json        # Debug configuration
├── addon/
│   ├── __init__.py        # Main add-on file
│   └── operators.py       # Example operators
├── specs/                 # PDD 2.0 specifications
│   ├── 00_system.md       # Global system prompts and rules
│   └── 01_arch.md         # Architectural context
├── scripts/               # PDD 2.0 build and sync tools
│   ├── builder.py         # The Architect - build code from specs
│   └── syncer.py          # The Fixer - sync specs from code
├── .venv/                 # Python virtual environment (created after setup)
├── .gitignore             # Git ignore rules
├── build_manifest.yaml    # PDD 2.0 feature manifest
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Prompt-Driven Development (PDD) 2.0

This template includes support for Prompt-Driven Development 2.0, a methodology for AI-assisted code generation and specification synchronization.

### What is PDD 2.0?

PDD 2.0 is a development workflow that:
- Maintains specifications alongside code
- Uses AI to generate code from specifications (forward workflow)
- Uses AI to update specifications from code changes (reverse workflow)
- Ensures consistency between documentation and implementation

### PDD 2.0 Components

#### Specifications (`specs/`)
- `00_system.md`: Global coding standards and rules
- `01_arch.md`: Architectural context and design decisions
- Feature specs: Detailed specifications for specific features (you add these)

#### Build Manifest (`build_manifest.yaml`)
Maps features to their specifications and target source files. This file tells the PDD tools which files are related to each feature.

#### PDD Tools (`scripts/`)

##### The Architect (`builder.py`)
Generates AI prompts for building code from specifications.

**Usage:**
```bash
# List all available features
python scripts/builder.py

# Generate prompt for a specific feature
python scripts/builder.py feature_name > prompt.txt
```

The generated prompt includes:
- Global context (coding standards, architecture)
- Feature specifications
- Current implementation (if any)
- Instructions for the AI

##### The Fixer (`syncer.py`)
Generates AI prompts for updating specifications from code changes.

**Usage:**
```bash
# List all available features
python scripts/syncer.py

# Generate sync prompt for a specific feature
python scripts/syncer.py feature_name > sync_prompt.txt
```

The generated prompt includes:
- Current code implementation (source of truth)
- Existing specifications (to be updated)
- Instructions for the AI to sync specs

### Using PDD 2.0 in Your Workflow

#### Forward Workflow: Spec → Code

1. Write a specification in `specs/features/my_feature.md`
2. Update `build_manifest.yaml` to map your feature to specs and target files
3. Run `python scripts/builder.py my_feature > prompt.txt`
4. Process the prompt with your preferred LLM (ChatGPT, Claude, local model, etc.)
5. Implement the generated code
6. Test in Blender

#### Reverse Workflow: Code → Spec

1. Modify code in `addon/`
2. Run `python scripts/syncer.py my_feature > sync_prompt.txt`
3. Process the prompt with your LLM
4. Update your specification files with the AI's output
5. Commit both code and updated specs together

#### Example: Adding a New Feature

```yaml
# Add to build_manifest.yaml
features:
  custom_mesh_tool:
    description: "Tool for creating custom mesh patterns"
    spec_files:
      - specs/features/custom_mesh_tool.md
    target_files:
      - addon/mesh_tools.py
    status: planned
```

Then use the builder to generate implementation prompts:
```bash
python scripts/builder.py custom_mesh_tool | pbcopy  # macOS
python scripts/builder.py custom_mesh_tool | xclip   # Linux
```

### Customizing PDD Tools

The provided scripts are templates designed for flexibility:
- They handle file reading and prompt formatting
- LLM API integration is left to you (add your preferred API)
- Customize prompt templates in the scripts as needed
- Supports any LLM: OpenAI, Anthropic, local models, etc.

## Customization

### Adding Your Add-on Code

1. Edit `addon/__init__.py` to define your add-on metadata and functionality
2. Add additional Python modules in the `addon/` directory as needed
3. Follow Blender add-on development best practices

### Adding Dependencies

To add Python packages to your development environment:

```bash
# Activate venv first
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\Activate.ps1  # Windows

# Install packages
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

## Troubleshooting

### Autocomplete Not Working

1. Ensure the Python extension selected the correct interpreter (`.venv/Scripts/python.exe` or `.venv/bin/python`)
2. Check that `fake-bpy-module-latest` is installed in your venv: `pip list | grep fake-bpy`
3. Restart VS Code if needed

### Blender Not Starting

1. Verify the `blender.blenderExecutable.path` in `.vscode/settings.json` points to your Blender executable
2. Check that the path exists and Blender can be launched from that location

### Debug Not Working

1. Ensure `blender.python.executable.path` points to your venv's Python executable
2. Make sure the Blender Development extension is installed and enabled

## Contributing

Feel free to submit issues and enhancement requests!

## License

This template is provided as-is for educational and development purposes.