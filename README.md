# Context Check
A command-line tool that tells you whether a document will fit into an AI model,
and roughly what it would cost to process. It works on a local text file or a web address.
## The problem
Businesses want to use AI models on their own documents: contracts, policies, reports.
Before they start, they ask two questions:
#1. **Will this document fit?** Every AI model can only read a limited number of tokens at
once.
#2. **What will it cost?** AI providers charge per token.
Context Check answers both in a second, without calling an AI model.
## Example
```text
$ python main.py https://dn790003.ca.archive.org/0/items/prideandprejudic42671gut/42671-8.txt
Characters: 763,082
Words: 130,416
Estimated tokens: 190,770
Estimated cost: $0.5723
Small (8K): TOO BIG
Standard (128K): TOO BIG
Large (200K): fits
Extra-large (1M): fits
Saved report.json
```
## Setup
You need Python 3.12 or newer and Git.
```bash
git clone https://github.com/Abdul-lah-Dev/context-check
cd context-check
python3 -m venv venv # Windows: python -m venv venv
source venv/bin/activate # Windows (Git Bash): source venv/Scripts/activate
pip install -r requirements.txt
```
## Usage
```bash
python main.py sample.txt # a local text file
python main.py https://example.com/doc.txt # a web address
python main.py # asks you for a file or address
```
The results are printed and also saved to `report.json`, so other programs can use them.
## How it works
-Loads the text from a file, or downloads it with `requests` (10-second timeout).
-Estimates tokens with a rule of thumb: about 4 characters per token for English.
-Estimates cost at an illustrative $3.00 per million tokens.
-Checks the token count against four context sizes stored in a dictionary.
-Gives a friendly message for missing files, non-text files and failed downloads.
## Limitations
-The token count is an **estimate**. Real models split text differently, and other
languages (such as Urdu) and code usually use more tokens.
-The price and the four context sizes are **illustrative**, not real model figures.
-Plain text only: PDF and Word files aren't supported yet.
## Next steps
-Count tokens exactly with a real tokenizer.
-Support PDF and Word documents.
-Send the document to an AI model and get a summary (Week 2).


## What I learned about tokens
A one-page policy is only about 600 tokens, so it fits every model. A short novel
like Alice in Wonderland is too big for an 8K model but fits easily in 128K. What
surprised me is that Pride and Prejudice doesn't even fit in 128K: a whole book
needs one of the largest models, or has to be split into parts.