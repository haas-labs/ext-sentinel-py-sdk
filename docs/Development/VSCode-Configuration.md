# VSCode Configuration

## Recommended

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