# AGENT INSTRUCTIONS

## Code style
- Use 4 spaces for indentation.
- Keep line length under 80 characters when possible.
- Use descriptive names and add a short docstring for new Python functions.

## Testing
- Run `pytest -q` from the repository root whenever Python code is modified.
- If files in `data/` are changed, run `node validate_dataset.js` to ensure the
  dataset is valid.

## Dependencies
- Python dependencies are listed in `requirements.txt`.
- Node dependencies are managed via `package.json`.
