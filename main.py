"""Context Check v0.2: will this document fit in an AI model, and what will it cost?"""

CHARS_PER_TOKEN = 4  # rule of thumb for English text
PRICE_PER_MILLION_TOKENS = 3.00  # illustrative USD rate per 1M input tokens


def estimate_tokens(text):
    """Roughly estimate how many tokens an AI model would see in this text."""
    return max(1, round(len(text) / CHARS_PER_TOKEN))


def estimate_cost(tokens):
    """Estimated input cost in US dollars at the illustrative rate."""
    return tokens / 1_000_000 * PRICE_PER_MILLION_TOKENS


text = input("Paste some text: ")
tokens = estimate_tokens(text)

print(f"Characters: {len(text)}")
print(f"Words: {len(text.split())}")
print(f"Estimated tokens: {tokens}")
print(f"Estimated cost: ${estimate_cost(tokens):.6f}")
