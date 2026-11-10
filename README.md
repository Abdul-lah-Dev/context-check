# Context Check

A small command-line tool that estimates whether a piece of text will fit into an AI model, and roughly what it would cost to process.

> Week 01 project — version 0.1

## Usage

```bash
python main.py
```

Paste some text when asked. The program prints the number of characters, words, estimated tokens and an estimated cost.

## Notes

- Tokens are estimated with a rule of thumb (about 4 characters per token for English text).
- The price per million tokens is illustrative, not a real model price.
