"""Context Check v0.2: will this document fit in an AI model, and what will it cost?"""

CHARS_PER_TOKEN = 4  # rule of thumb for English text
PRICE_PER_MILLION_TOKENS = 3.00  # illustrative USD rate per 1M input tokens

CONTEXT_TIERS = {
    "Small (8K)": 8_000,
    "Standard (128K)": 128_000,
    "Large (200K)": 200_000,
    "Extra-large (1M)": 1_000_000,
}


def estimate_tokens(text):
    """Roughly estimate how many tokens an AI model would see in this text."""
    return max(1, round(len(text) / CHARS_PER_TOKEN))


def estimate_cost(tokens):
    """Estimated input cost in US dollars at the illustrative rate."""
    return tokens / 1_000_000 * PRICE_PER_MILLION_TOKENS


def check_tiers(tokens):
    """Return a dict of tier name -> True/False (does the text fit?)."""
    results = {}
    for name, limit in CONTEXT_TIERS.items():
        results[name] = tokens <= limit
    return results


def load_text(path):
    """Read a text file and return everything in it as one string."""
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def main():
    path = input("Document to check: ").strip()
    text = load_text(path)
    tokens = estimate_tokens(text)

    print(f"Characters: {len(text):,}")
    print(f"Words: {len(text.split()):,}")
    print(f"Estimated tokens: {tokens:,}")
    print(f"Estimated cost: ${estimate_cost(tokens):.4f}")
    for tier, fits in check_tiers(tokens).items():
        if fits:
            print(f"  {tier}: fits")
        else:
            print(f"  {tier}: TOO BIG")


main()
