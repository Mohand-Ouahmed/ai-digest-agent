"""Tests pour Summarizer, avec un client LLM mocke (aucun appel reseau)."""
from __future__ import annotations

import pytest

from ai_digest_agent.config import Config
from ai_digest_agent.sources import Item
from ai_digest_agent.summarizer import Summarizer, SummarizationError


class FakeLlmClient:
    """Double de test : renvoie une reponse fixe ou echoue a la demande."""

    def __init__(self, responses=None, fail_times: int = 0):
        self._responses = list(responses or [])
        self._fail_times = fail_times
        self.calls = 0

    def complete(self, prompt: str) -> str:
        self.calls += 1
        if self.calls <= self._fail_times:
            raise RuntimeError("erreur simulee du LLM")
        return self._responses.pop(0) if self._responses else "resume simule"


def make_config(max_retries: int = 3) -> Config:
    return Config(anthropic_api_key="test-key", max_retries=max_retries)


def test_summarize_returns_summary_on_first_success():
    client = FakeLlmClient(responses=["Un resume clair."])
    summarizer = Summarizer(client=client, config=make_config())
    item = Item(title="Titre", content="Contenu", url="https://example.com")

    result = summarizer.summarize(item)

    assert result.title == "Titre"
    assert result.summary == "Un resume clair."
    assert result.source_url == "https://example.com"
    assert client.calls == 1


def test_summarize_retries_after_transient_failure(monkeypatch):
    monkeypatch.setattr("ai_digest_agent.summarizer.time.sleep", lambda _seconds: None)
    client = FakeLlmClient(responses=["Ca marche."], fail_times=2)
    summarizer = Summarizer(client=client, config=make_config(max_retries=3))
    item = Item(title="Titre", content="Contenu", url="https://example.com")

    result = summarizer.summarize(item)

    assert result.summary == "Ca marche."
    assert client.calls == 3


def test_summarize_raises_after_exhausting_retries(monkeypatch):
    monkeypatch.setattr("ai_digest_agent.summarizer.time.sleep", lambda _seconds: None)
    client = FakeLlmClient(fail_times=99)
    summarizer = Summarizer(client=client, config=make_config(max_retries=2))
    item = Item(title="Titre", content="Contenu", url="https://example.com")

    with pytest.raises(SummarizationError):
        summarizer.summarize(item)

    assert client.calls == 2
