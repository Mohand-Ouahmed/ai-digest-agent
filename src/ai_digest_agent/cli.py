"""Point d'entree en ligne de commande de l'agent de veille."""
from __future__ import annotations

import argparse
import sys

from ai_digest_agent.config import Config, MissingConfigError
from ai_digest_agent.sources import RssSource
from ai_digest_agent.summarizer import Summarizer


class AnthropicClient:
    """Client LLM base sur l'API Anthropic (Claude)."""

    def __init__(self, api_key: str, model: str):
        from anthropic import Anthropic

        self._client = Anthropic(api_key=api_key)
        self._model = model

    def complete(self, prompt: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text


def build_digest(feed_url: str, max_items: int) -> str:
    config = Config.from_env()
    client = AnthropicClient(api_key=config.anthropic_api_key, model=config.model)
    summarizer = Summarizer(client=client, config=config)
    source = RssSource(feed_url=feed_url, max_items=max_items)

    lines = ["# Digest technique", ""]
    for item in source.fetch():
        summary = summarizer.summarize(item)
        lines.append(f"## {summary.title}")
        lines.append(summary.summary)
        lines.append(f"[Source]({summary.source_url})")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genere un digest technique a partir d'un flux RSS."
    )
    parser.add_argument("feed_url", help="URL du flux RSS/Atom a resumer")
    parser.add_argument(
        "--max-items", type=int, default=5, help="Nombre maximum d'articles a traiter"
    )
    parser.add_argument(
        "--output", default="digest.md", help="Fichier de sortie (defaut: digest.md)"
    )
    args = parser.parse_args()

    try:
        digest = build_digest(args.feed_url, args.max_items)
    except MissingConfigError as exc:
        print(f"Erreur de configuration : {exc}", file=sys.stderr)
        return 1

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(digest)
    print(f"Digest ecrit dans {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
