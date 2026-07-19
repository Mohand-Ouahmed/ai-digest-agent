# ai-digest-agent

Agent de veille technique : recupere des sources (flux RSS), les resume via un LLM avec des prompts structures, et produit un digest lisible. Pense comme reference d'architecture pour des agents IA de production : configuration par variables d'environnement, retry avec backoff, sortie testable sans appel reseau reel.

Ce depot est un exemple generique, decouple de tout projet client ou personnel.

## Pourquoi ce projet

La plupart des demos d'agents IA sont des scripts jetables : cle API en dur, aucun test, aucune gestion d'erreur. Ce depot montre une structure minimale mais serieuse : separation claire entre recuperation des sources, appel au LLM et presentation, avec des points d'extension explicites.

## Architecture

| Module | Role |
| --- | --- |
| `config` | Chargement de la configuration depuis l'environnement, echoue explicitement si une cle manque |
| `sources` | Recuperation des elements a resumer (flux RSS par defaut, interface remplacable) |
| `summarizer` | Appel au LLM avec prompt structure, retry avec backoff exponentiel |
| `cli` | Point d'entree : assemble les modules, gere les arguments de la ligne de commande |

## Installation

```bash
pip install -e .
```

Copier `.env.example` vers `.env` et renseigner `ANTHROPIC_API_KEY`. Aucune cle n'est jamais commitee : `.env` est ignore par git.

## Utilisation

```bash
ai-digest-agent https://blog.example.com/feed.xml --max-items 5 --output digest.md
```

Variables d'environnement optionnelles : `AI_DIGEST_MODEL` (modele utilise) et `AI_DIGEST_MAX_RETRIES` (nombre de tentatives).

## Tests

```bash
pip install -e ".[dev]"
pytest
```

Les tests du summarizer utilisent un client LLM factice (mock) : ils s'executent sans cle API et sans appel reseau, ce qui les rend rapides et deterministes.

## Points d'extension

Ajouter une nouvelle source : implementer l'interface `Source` dans `sources.py` (API, base de donnees, scraping).

Changer de fournisseur LLM : le module `summarizer` isole l'appel reseau derriere l'interface `LlmClient`, facilement substituable.

Ajouter un format de sortie : `build_digest` renvoie du texte ; brancher un autre rendu (JSON, email, Slack) revient a remplacer l'ecriture du fichier dans `cli.py`.

---

Exemple d'architecture realise par Mohand Abellache, Solutions & Applications Architect.
