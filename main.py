"""Context Check v2-alpha: measure a document, then ask an AI model to summarise it.

Works with any provider that speaks the OpenAI API format (Gemini, OpenAI, Claude,
Groq, OpenRouter, Ollama). Settings live in .env (see .env.example).

Usage:
    python main.py sample.txt
    python main.py https://www.gutenberg.org/cache/epub/1342/pg1342.txt
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv
from openai import OpenAI

CHARS_PER_TOKEN = 4  # rule of thumb for English text
PRICE_PER_MILLION_TOKENS = 3.00  # illustrative USD rate per 1M input tokens

CONTEXT_TIERS = {
    "Small (8K)": 8_000,
    "Standard (128K)": 128_000,
    "Large (200K)": 200_000,
    "Extra-large (1M)": 1_000_000,
}

PRICES = {  # US dollars per million tokens: (input, output). Check your provider's page.
    "gemini-4-hydrogen": (1.50, 7.50),  # free tier in AI Studio: this is the paid price
    "gemini-3.5-flash-lite": (0.30, 2.50),
    "gpt-5-nano": (0.05, 0.40),
    "claude-haiku-5-5": (0.10, 0.50),
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


def load_text(source):
    """Load text from a web address (http/https) or from a local file."""
    if source.startswith("http://") or source.startswith("https://"):
        response = requests.get(source, timeout=10)
        response.raise_for_status()  # turns 4xx / 5xx status codes into an error
        return response.text
    with open(source, "r", encoding="utf-8") as file:
        return file.read()


def build_report(source, text):
    """Collect everything we know about the document in one dictionary."""
    tokens = estimate_tokens(text)
    return {
        "source": source,
        "characters": len(text),
        "words": len(text.split()),
        "estimated_tokens": tokens,
        "estimated_cost_usd": round(estimate_cost(tokens), 4),
        "fits": check_tiers(tokens),
    }


def save_report(report, path="report.json"):
    """Write the report to a JSON file that other programs can read."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)


def summarise(client, model, text):
    """Ask the AI model for a short summary. Return (summary, usage)."""
    prompt = ("Summarise this document in 5 short bullet points.\n\n"
              f"<document>\n{text}\n</document>")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content, response.usage


def cost_of(model, usage):
    """Dollar cost of one call from the real token counts (0 if the model isn't in PRICES)."""
    price_in, price_out = PRICES.get(model, (0.0, 0.0))
    return (usage.prompt_tokens * price_in + usage.completion_tokens * price_out) / 1_000_000


def main():
    if len(sys.argv) > 1:
        source = sys.argv[1]
    else:
        source = input("File or web address to check: ").strip()

    try:
        text = load_text(source)
    except FileNotFoundError:
        print(f"Could not find {source}. Check the name and the folder you are in.")
        return
    except UnicodeDecodeError:
        print(f"{source} doesn't look like a plain text file.")
        return
    except requests.exceptions.RequestException as error:
        print(f"Could not download {source}")
        print(f"Reason: {error}")
        return

    if not text.strip():
        print(f"{source} is empty. There is nothing to check.")
        return

    report = build_report(source, text)

    print(f"Characters: {report['characters']:,}")
    print(f"Words: {report['words']:,}")
    print(f"Estimated tokens: {report['estimated_tokens']:,}")
    print(f"Estimated cost: ${report['estimated_cost_usd']:.4f}")
    for tier, fits in report["fits"].items():
        if fits:
            print(f"  {tier}: fits")
        else:
            print(f"  {tier}: TOO BIG")

    save_report(report)
    print("Saved report.json")

    load_dotenv()
    client = OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=os.environ["LLM_BASE_URL"])
    model = os.environ["LLM_MODEL"]
    summary, usage = summarise(client, model, text)

    print(f"\nSummary from {model}:")
    print(summary)
    print(f"Real tokens: {usage.prompt_tokens:,} in · {usage.completion_tokens:,} out")
    print(f"Real cost: ${cost_of(model, usage):.4f}  (estimate was {report['estimated_tokens']:,} tokens)")


main()