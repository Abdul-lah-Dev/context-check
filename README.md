# Context Check

A small command-line tool that estimates whether a document will fit into an AI model, and roughly what it would cost to process.

> Week 01 project — version 0.2

## Usage

```bash
python main.py
```

Type the name of a plain text file (for example `sample.txt`) when asked. The program prints:

- the number of characters and words
- the estimated number of tokens and the estimated cost
- whether the document fits into four model context sizes: 8K, 128K, 200K and 1M tokens

If the file can't be found, or isn't a plain text file, it prints a friendly message instead of crashing.

## Notes

- Tokens are estimated with a rule of thumb (about 4 characters per token for English text).
- The price per million tokens and the context sizes are illustrative, not real model figures.
