# AI Agent Conversation Codebase Guide

## Development Commands
- Run server: `./dev.sh` or `fastapi dev app/main.py`
- Setup environment: `./setup.sh`
- Install dependencies: `pip install -r requirements.txt`
- Activate virtual environment: `source .venv/bin/activate`

## Code Style Guidelines
- **Imports**: Group imports by standard library, third-party, and local modules with a blank line between groups
- **Structure**: Follow FastAPI router pattern for API endpoints
- **Naming**: 
  - Use snake_case for variables, functions, and file names
  - Use PascalCase for class names
- **Type Hints**: Always include type hints for function parameters and return values
- **Documentation**: Include docstrings for public functions and classes
- **Error Handling**: Use try/except blocks with specific exception types
- **Template Files**: Store HTML templates in app/frontend directory
- **Config**: Store configuration in app/core/config.py and constants in app/core/constants.py
- **Backend Logic**: Separate API routes (app/api) from feature implementation (app/features)