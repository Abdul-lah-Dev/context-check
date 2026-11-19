# Context Check Lab (v0.2)

A command-line Python utility that reads a plain text document, estimates its character count, word count, token count, and processing cost, and checks whether it fits inside common AI model context windows.

## Features

* Reads plain text files with UTF-8 encoding
* Estimates tokens using a 4-characters-per-token rule of thumb (minimum 1 token)
* Calculates estimated input cost per 1 million tokens
* Evaluates compatibility across four model context tiers (`Small (8K)`, `Standard (128K)`, `Large (200K)`, and `Extra-large (1M)`)
* Handles missing files, non-text files, and empty files with clear messages instead of crashing

## Setup & Usage

1. Navigate to the project folder in Git Bash:
   `cd "/d/AI Solutions Engineering/Session 2/context-check-lab"`

2. Create and activate a virtual environment:
   `python -m venv venv`
   `source venv/Scripts/activate`

3. Add text to `sample.txt`, then run the program:
   `python main.py`

4. Enter the file name when prompted (for example, `sample.txt`).

## Project Files

* `main.py` — Token estimation, cost calculation, tier checking, file loading, error handling, and CLI entry point
* `sample.txt` — Sample plain text document for testing
* `.gitignore` — Excludes virtual environments and temporary/cache files from Git
* `README.md` — Project overview and usage instructions