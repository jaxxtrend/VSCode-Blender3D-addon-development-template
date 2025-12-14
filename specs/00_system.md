# System Prompts and Global Rules

## Purpose
This document defines the global system prompts and rules that apply to all development work in this project. These rules ensure consistency, quality, and adherence to best practices across the codebase.

## Development Environment
- **Target Platform**: Blender 3.x+ Add-on Development
- **Primary Language**: Python 3.10+
- **Development IDE**: Visual Studio Code with Blender Development Extension
- **Virtual Environment**: Python venv for isolated dependency management

## Coding Standards

### Python Style Guide
- Follow PEP 8 style guidelines
- Use Black formatter for code formatting (line length: 88 characters)
- Maximum line length for comments and docstrings: 88 characters
- Use type hints where appropriate for better IDE support

### Code Quality
- Run `pylint` on all Python code before committing
- Maintain a pylint score of 8.0/10 or higher
- Use meaningful variable and function names
- Write docstrings for all classes and non-trivial functions

### Blender Add-on Specific Rules
- Use proper Blender naming conventions (e.g., `CATEGORY_OT_operation` for operators)
- Always implement `bl_idname`, `bl_label`, and `bl_description` for operators and panels
- Use `bl_options = {"REGISTER", "UNDO"}` for operators that modify scene data
- Properly implement `register()` and `unregister()` functions

## Project Structure Rules

### Directory Organization
```
project-root/
├── specs/          # PDD 2.0 specifications
├── scripts/        # PDD 2.0 build and sync tools
├── addon/          # Blender add-on source code
├── .vscode/        # VS Code workspace settings
└── .venv/          # Python virtual environment (not committed)
```

### File Organization
- Keep add-on code organized in the `addon/` directory
- Split large add-ons into multiple modules (operators, panels, properties, etc.)
- Import and register all classes in `addon/__init__.py`

## Version Control

### Git Practices
- Write clear, descriptive commit messages
- Keep commits focused and atomic
- Never commit the `.venv/` directory or `__pycache__/` files
- Update `.gitignore` to exclude generated files

### Branch Strategy
- Use feature branches for new development
- Name branches descriptively (e.g., `feature/new-operator`, `fix/bug-description`)

## Testing and Validation

### Before Committing
1. Format code with Black: `black addon/`
2. Lint code with pylint: `pylint addon/ --disable=import-error`
3. Test the add-on in Blender
4. Verify no errors in Blender console

### Code Review Guidelines
- Ensure code follows all style guidelines
- Verify proper error handling
- Check that operators provide user feedback via `self.report()`
- Confirm that undo/redo works correctly for operators

## Documentation Requirements

### Code Documentation
- Include module-level docstrings explaining the purpose of each file
- Document complex algorithms and non-obvious logic
- Use clear, concise comments

### User Documentation
- Keep README.md up to date with setup instructions
- Document any new features or operators in the README
- Provide examples of how to use new functionality

## Security and Best Practices

### Dependency Management
- Pin dependencies in `requirements.txt`
- Only include necessary dependencies
- Regularly update dependencies to address security vulnerabilities

### Error Handling
- Always handle potential errors gracefully
- Provide meaningful error messages to users
- Log errors appropriately for debugging

## PDD 2.0 Workflow

### Using the Builder (The Architect)
- Use `scripts/builder.py` to generate code from specifications
- Review and test generated code before committing
- Iterate on specifications if generated code needs refinement

### Using the Syncer (The Fixer)
- Use `scripts/syncer.py` to update specifications after code changes
- Ensure specifications stay synchronized with implementation
- Run syncer after significant code refactoring

### Specification Writing
- Write clear, unambiguous specifications
- Include expected behavior and edge cases
- Reference relevant architectural decisions from `specs/01_arch.md`
- Use examples to illustrate complex behavior
