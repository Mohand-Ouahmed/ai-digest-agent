"""Appel au LLM avec prompt structure et retry.

Le client est isole derriere Summarizer pour rester substituable (autre
fournisseur, ou double de test) sans toucher au reste du code.
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol

from ai_digest_agent.config import Config
from ai_digest_agent.sources import Item

PROMPT_TEMPLATE = """Tu resumes un article technique en 3 phrases maximum,
en francais, pour un lecteur developpeur/architecte pressee.

Titre : {title}
Contenu : {content}

Reponds uniquement avec le resume, sans preambule."""


class LlmClient(Protocol):
    """Interface minimale attendue d'un client LLM."""

    def complete(self, prompt: str) -> str: ...


@dataclass
class Summary:
    title: str
    summary: str
    source_url: str


class SummarizationError(RuntimeError):
    """Levee quand le LLM echoue apres tous les essais."""


class Summarizer:
    def __init__(self, client: LlmClient, config: Config):
        self._client = client
        self._config = config

    def summarize(self, item: Item) -> Summary:
        prompt = PROMPT_TEMPLATE.format(title=item.title, content=item.content)
        text = self._call_with_retry(prompt)
        return Summary(title=item.title, summary=text.strip(), source_url=item.url)

    def _call_with_retry(self, prompt: str) -> str:
        last_error: Exception | None = None
        for attempt in range(self._config.max_retries):
            try:
                return self._client.complete(prompt)
            except Exception as exc:
                last_error = exc
                if attempt < self._config.max_retries - 1:
                    time.sleep(2**attempt)
        raise SummarizationError(
            f"Echec apres {self._config.max_retries} tentatives"
        ) from last_error
