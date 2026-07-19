"""Sources de veille : recuperation d'articles a resumer.

Definit le contrat Source (Protocol) et l'implementation RSS de reference.
Chaque source produit une liste d'Item, decouple du reste du pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import feedparser


@dataclass
class Item:
    title: str
    content: str
    url: str


class Source(Protocol):
    """Interface minimale attendue d'une source d'articles."""

    def fetch(self) -> list[Item]: ...


class RssSource:
    """Source basee sur un flux RSS/Atom (via feedparser)."""

    def __init__(self, feed_url: str, max_items: int = 5):
        self._feed_url = feed_url
        self._max_items = max_items

    def fetch(self) -> list[Item]:
        parsed = feedparser.parse(self._feed_url)
        items = []
        for entry in parsed.entries[: self._max_items]:
            items.append(
                Item(
                    title=entry.get("title", "Sans titre"),
                    content=entry.get("summary", ""),
                    url=entry.get("link", ""),
                )
            )
        return items
