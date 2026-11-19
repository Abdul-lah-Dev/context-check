


CHARS_PER_TOKEN = 4
PRICE_PER_MILLION_TOKENS = 3.00

CONTEXT_TIERS = {
    "Small (8K)": 8_000,
    "Standard (128K)": 128_000,
    "Large (200K)": 200_000,
    "Extra-large (1M)": 1_000_000,
}

def estimate_tokens (text):
    return max (1, round(len(text) / CHARS_PER_TOKEN))


def estimate_cost (tokens):
    return tokens / 1_000_000 * PRICE_PER_MILLION_TOKENS


def check_tiers (tokens):
    results = {}
    for name, limit in CONTEXT_TIERS.items():
        results[name] = tokens <= limit
    return results


def load_text (path):
    with open(path, "r", encoding = "utf-8") as file:
        return file.read()


def main():
    path = input("Document to check: ").strip()

    try:
        text = load_text(path)
    except FileNotFoundError:
        print(f"Could not find {path}. Check the name and the folder you are in.")
        return
    except UnicodeDecodeError:
        print(f"{path} doesn't look like a plain text file.")
        return

    if not text.strip():
        print(f"{path} is empty. There is nothing to check.")
        return

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