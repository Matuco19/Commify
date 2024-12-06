# Contributing to Commify

Thank you for considering contributing to Commify! We value your time and effort and appreciate your contributions. By participating in this project, you agree to adhere to our [Code of Conduct](#code-of-conduct) and [MATCO-Open-Source](https://matuco19.com/licenses/MATCO-Open-Source) License.

## Table of Contents
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting Changes](#submitting-changes)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Code of Conduct](#code-of-conduct)

---

## Getting Started

1. Fork the repository and clone it to your local machine.
2. Make sure you have Python installed (version 3.8 or higher).
3. Install the required dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

## How to Contribute

### Reporting Bugs
1. Ensure the issue does not already exist in the [Issues tab](https://github.com/Matuco19/Commify/issues).
2. Create a new issue and include:
   - A descriptive title.
   - Steps to reproduce the issue.
   - The expected vs actual behavior.
   - Any relevant logs or screenshots.

### Suggesting Features
1. Open a new issue with the "Feature Request" label.
2. Clearly describe:
   - What the feature does.
   - Why it would be beneficial.
   - Any implementation suggestions.

### Submitting Changes
1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes, adhering to the [Code Style Guidelines](#code-style-guidelines).
3. Commit your changes with a clear and descriptive commit message:
   ```bash
   git commit -m "Add: Detailed description of your change"
   ```
4. Push your branch to your forked repository:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Create a pull request to the `main` branch and include:
   - A clear title and description of your changes.
   - Reference any relevant issues (e.g., "Fixes #42").

---

## Development Setup

1. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```
2. Run tests to ensure your changes don’t break existing functionality:
   ```bash
   python -m unittest discover
   ```
3. Verify your code with linters:
   ```bash
   flake8
   ```

---

## Code Style Guidelines

Commify follows the [PEP 8](https://peps.python.org/pep-0008/) style guide. Please ensure:
- Indentation is 4 spaces.
- Functions and variable names are descriptive.
- Docstrings are used for all public methods and classes.

Use tools like [Black](https://black.readthedocs.io/en/stable/) and [isort](https://pycqa.github.io/isort/) for consistent formatting:
```bash
black .
isort .
```

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

---

We look forward to your contributions! If you have any questions, feel free to contacting the maintainers directly.
