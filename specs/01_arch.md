# Architectural Context

## Project Overview

This is a VS Code Blender Add-on Development Template that provides a ready-to-use environment for developing Blender 3D add-ons with full IDE support, autocomplete, debugging, and hot reload capabilities.

## Architecture Goals

1. **Developer Experience**: Provide seamless integration between VS Code and Blender
2. **Type Safety**: Enable full autocomplete and type checking for Blender API
3. **Rapid Development**: Support hot reload for immediate feedback during development
4. **Professional Tooling**: Include linting, formatting, and debugging out of the box
5. **Extensibility**: Allow easy adaptation for specific add-on requirements

## System Components

### 1. Development Environment Setup

#### Virtual Environment
- **Location**: `.venv/` directory (not version controlled)
- **Purpose**: Isolate project dependencies from system Python
- **Key Dependencies**:
  - `fake-bpy-module-latest`: Provides Blender API type stubs
  - `black`: Code formatter
  - `pylint`: Code linter
  - `mypy`: Type checker
  - `PyYAML`: YAML parsing for PDD 2.0 manifest

#### Setup Script (`setup.py`)
- **Purpose**: Automate initial environment setup
- **Responsibilities**:
  - Create virtual environment
  - Install dependencies
  - Configure VS Code settings for current platform
- **Platform Support**: Windows, macOS, Linux

### 2. Add-on Source Code

#### Main Add-on Module (`addon/__init__.py`)
- **Purpose**: Entry point for the Blender add-on
- **Contains**:
  - `bl_info` dictionary with add-on metadata
  - Operator and Panel class definitions
  - `register()` and `unregister()` functions
- **Design Pattern**: All classes collected in `classes` list for easy registration

#### Additional Modules (`addon/operators.py`, etc.)
- **Purpose**: Organize code into logical modules
- **Pattern**: Import and extend `classes` list in `__init__.py`
- **Benefit**: Keeps codebase maintainable as add-on grows

### 3. VS Code Integration

#### Workspace Settings (`.vscode/settings.json`)
- **Python Configuration**:
  - Points to virtual environment Python interpreter
  - Configures extra paths for Blender API autocomplete
- **Blender Extension Configuration**:
  - Path to Blender executable
  - Addon development settings
  - Hot reload on save enabled

#### Debug Configuration (`.vscode/launch.json`)
- **Blender: Launch & Debug**: Configuration for debugging add-on in Blender
- **Features**:
  - Breakpoint support
  - Variable inspection
  - Step-through debugging

### 4. PDD 2.0 Support (Prompt-Driven Development)

#### Specifications Directory (`specs/`)
- **00_system.md**: Global system prompts and coding standards
- **01_arch.md**: This file - architectural context
- **Feature Specs**: Additional specs for specific features (to be added)

#### Build Manifest (`build_manifest.yaml`)
- **Purpose**: Map features to specifications and target files
- **Structure**:
  - `global_context`: References to system and architecture specs
  - `features`: Dictionary mapping feature names to their specs and targets

#### PDD Tools (`scripts/`)

##### The Architect (`scripts/builder.py`)
- **Purpose**: Generate code from specifications
- **Workflow**:
  1. Parse `build_manifest.yaml`
  2. Read relevant specifications
  3. Read existing target files (if any)
  4. Prepare AI prompt with context
  5. Output prompt for LLM processing
- **Design**: Template/scaffold for user's LLM integration

##### The Fixer (`scripts/syncer.py`)
- **Purpose**: Update specifications from code changes
- **Workflow**:
  1. Parse `build_manifest.yaml`
  2. Read modified target files
  3. Read current specifications
  4. Prepare reverse-sync prompt
  5. Output prompt for LLM processing
- **Design**: Template/scaffold for user's LLM integration

## Data Flow

### Development Workflow
```
Developer writes code in addon/
    ↓
VS Code saves file
    ↓
Blender Development Extension detects change
    ↓
Add-on automatically reloads in Blender
    ↓
Developer tests in Blender
    ↓
Repeat
```

### PDD 2.0 Workflow (Forward: Spec → Code)
```
Developer writes specification in specs/
    ↓
Updates build_manifest.yaml with feature mapping
    ↓
Runs scripts/builder.py
    ↓
Reviews generated AI prompt
    ↓
Processes prompt with LLM (user's choice of tool)
    ↓
Implements generated code
    ↓
Tests in Blender
```

### PDD 2.0 Workflow (Reverse: Code → Spec)
```
Developer modifies code in addon/
    ↓
Runs scripts/syncer.py
    ↓
Reviews generated sync prompt
    ↓
Processes prompt with LLM (user's choice of tool)
    ↓
Updates specification files
    ↓
Commits both code and specs
```

## Technology Stack

### Core Technologies
- **Python 3.10+**: Development language
- **Blender 3.x+**: Target platform
- **VS Code**: Development IDE

### Development Dependencies
- **fake-bpy-module**: Blender API stubs for autocomplete
- **black**: Automatic code formatting
- **pylint**: Code quality checking
- **mypy**: Static type checking
- **PyYAML**: YAML parsing for manifests

### VS Code Extensions
- **Python** (Microsoft): Python language support
- **Blender Development** (Jacques Lucke): Blender integration

## Design Decisions

### Why Virtual Environment?
- Isolates project dependencies
- Enables different Blender API versions per project
- Prevents conflicts with system Python packages
- Allows team members to have consistent environments

### Why fake-bpy-module?
- Blender's `bpy` module only exists within Blender
- Cannot import `bpy` in external Python for type checking
- `fake-bpy-module` provides type stubs for IDE autocomplete
- Enables static analysis without running Blender

### Why PDD 2.0 Scripts as Templates?
- LLM API landscape is diverse (OpenAI, Anthropic, local models, etc.)
- Users have different preferences and requirements
- Templates provide file reading/parsing logic
- Users add their preferred LLM integration
- Keeps template flexible and not locked to one provider

### Platform-Specific Configuration
- Python path formats differ (Windows vs Unix)
- Blender installation paths vary by platform
- `setup.py` automatically configures for current platform
- Reduces setup friction for developers

## Extension Points

### Adding New Operators
1. Define operator class in `addon/` (in `__init__.py` or separate module)
2. Add to `classes` list
3. Optionally add to a Panel for UI access

### Adding New Modules
1. Create new `.py` file in `addon/`
2. Import in `addon/__init__.py`
3. Extend `classes` list with module's classes

### Adding PDD 2.0 Features
1. Write specification in `specs/`
2. Update `build_manifest.yaml` with feature entry
3. Run `scripts/builder.py` to generate prompt
4. Implement generated code

### Customizing PDD Tools
1. Modify `scripts/builder.py` or `scripts/syncer.py`
2. Add LLM API integration
3. Customize prompt templates
4. Add additional context gathering logic

## Quality Assurance

### Automated Checks
- Black formatting (enforced)
- Pylint linting (target: 8.0/10+)
- Type checking with mypy (optional)

### Manual Testing
- Load add-on in Blender
- Test all operators and panels
- Verify undo/redo functionality
- Check console for errors

### Code Review Guidelines
- Verify adherence to coding standards (see `specs/00_system.md`)
- Check for proper error handling
- Ensure user feedback via `self.report()`
- Validate that changes don't break existing functionality

## Future Considerations

### Potential Enhancements
- Automated testing framework for Blender add-ons
- CI/CD pipeline for automated testing
- Add-on packaging and distribution tools
- Template variants for different add-on types (import/export, tools, etc.)
- Integration examples with various LLM APIs

### Scalability
- Current architecture supports small to medium add-ons
- For large add-ons, consider:
  - More granular module structure
  - Separation of UI and logic
  - Configuration file for add-on settings
  - Asset management strategy
