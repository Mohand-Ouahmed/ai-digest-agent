# ai-digest-agent

Agent de veille technique : recupere des sources (flux RSS), les resume via un LLM avec des prompts structures, et produit un digest lisible. Pense comme reference d'architecture pour des agents IA de production : configuration par variables d'environnement, retry avec backoff, sortie testable sans appel reseau reel.

Ce depot est un exemple generique, decouple de tout projet client ou personnel.

## Pourquoi ce projet

La plupart des demos d'agents IA sont des scripts jetables : cle API en dur, aucun test, aucune gestion d'erreur. Ce depot montre une structure minimale mais serieuse : separation claire entre recuperation des sources, appel au LLM et presentation, avec des points d'extension explicites.

## Architecture

config          chargement de la configuration depuis l'environnement, echoue explicitement si une cle manque

sources         recuperation des elements a resumer (flux RSS par defaut, interface remplacable)

summarizer      appel au LLM avec prompt structure, retry avec backoff exponentiel, parsing de la reponse

cli             point d'entree : assemble les modules, gere les arguments de la ligne de commande

## Installation

pip install -e .

Copier .env.example vers .env et renseigner ANTHROPIC_API_KEY. Aucune cle n'est jamais commitee : .env est ignore par git.

## Utilisation

ai-digest-agent --topics "architecture logicielle,IA generative" --output digest.md

## Tests

pytest

Les tests du summarizer utilisent un client LLM factice (mock) : ils s'executent sans cle API et sans appel reseau, ce qui les rend rapides et deterministes.

## Points d'extension

Ajouter une nouvelle source : implementer l'interface Source dans sources.py (API, base de donnees, scraping).

Changer de fournisseur LLM : le module summarizer isole l'appel reseau derriere une interface simple, facilement substituable.

Ajouter un format de sortie : le CLI accepte un writer configurable (markdown, JSON, envoi email/Slack).

---
Exemple d'architecture realise par Mohand Abellache, Solutions & Applications Architect.
