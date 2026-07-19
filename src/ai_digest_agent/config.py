"""Configuration chargee depuis l'environnement.

Echoue explicitement (au demarrage, pas en cours d'execution) si une
variable requise est absente -- pas de comportement silencieux degrade.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_MODEL = "claude-sonnet-5"
DEFAULT_MAX_RETRIES = 3


class MissingConfigError(RuntimeError):
    """Levee quand une variable d'environnement requise est absente."""


@dataclass(frozen=True)
class Config:
    anthropic_api_key: str
    model: str = DEFAULT_MODEL
    max_retries: int = DEFAULT_MAX_RETRIES

    @staticmethod
    def from_env() -> "Config":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise MissingConfigError(
                "ANTHROPIC_API_KEY manquant. Copiez .env.example vers .env "
                "et renseignez une cle valide."
            )
        return Config(
            anthropic_api_key=api_key,
            model=os.environ.get("AI_DIGEST_MODEL", DEFAULT_MODEL),
            max_retries=int(os.environ.get("AI_DIGEST_MAX_RETRIES", DEFAULT_MAX_RETRIES)),
        )
