"""Context Check v0.1 — will this text fit in an AI model, and what will it cost?

Paste some text and get a character count, a word count, an estimated
number of tokens, and an estimated cost.
"""

CHARS_PER_TOKEN = 4  # rule of thumb for English text
PRICE_PER_MILLION_TOKENS = 3.00  # illustrative USD rate per 1M input tokens

text = input("Paste some text: ")

chars = len(text)
words = len(text.split())
tokens = round(chars / CHARS_PER_TOKEN)
cost = tokens / 1_000_000 * PRICE_PER_MILLION_TOKENS

print(f"Characters: {chars}")
print(f"Words: {words}")
print(f"Estimated tokens: {tokens}")
print(f"Estimated cost: ${cost:.6f}")
