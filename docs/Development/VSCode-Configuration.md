# VSCode Configuration

## Recommended

This guide outlines common VSCode settings for Python development, along with the requirement to install Python and Ruff.

Note: Before applying these settings, ensure that Python and Ruff are installed on your system.

Extentions required:
- Python: provides support for Python language features and tools
- Ruff: A code formatter for Python that enforces PEP 8 style guide recommendations. 

`.vscode/settings.json`

```json
{
    "[python]": {
        // Automatically format the code when saving a file
        "editor.formatOnSave": true,
        // Configure code actions to perform on save
        "editor.codeActionsOnSave": {
            // Perform all available fixes on save
            "source.fixAll": "explicit",
            // Organize imports on save
            "source.organizeImports": "explicit",
        },
        // Set default code formatter to Ruff, it should be installed
        "editor.defaultFormatter": "charliermarsh.ruff"
    },
    // Display a vertical ruler at column 120 to help maintain PEP 8 style guide recommendations
    "editor.rulers": [120]
}
```

Since all Sentinel documentation is Markdown based, it would be helpful to add

```json
    "[markdown]": {
        "editor.wordWrap": "bounded",
        "editor.wordWrapColumn": 120
    },
```
