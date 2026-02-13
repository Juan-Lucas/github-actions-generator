# GitHub Actions Generator

[![PyPI version](https://badge.fury.io/py/gha-generator.svg)](https://badge.fury.io/py/gha-generator)
[![Python](https://img.shields.io/pypi/pyversions/gha-generator.svg)](https://pypi.org/project/gha-generator/)
[![License](https://img.shields.io/pypi/l/gha-generator.svg)](https://github.com/Juan-Lucas/github-actions-generator/blob/main/LICENSE)

Un outil CLI pour générer des workflows GitHub Actions personnalisés et standardisés.

## Description

GitHub Actions Generator automatise la création de fichiers YAML pour GitHub Actions. Il permet de standardiser et d'accélérer la mise en place des pipelines CI/CD pour différents environnements techniques (Data Science, Django, Laravel, React).

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip

### Installation

#### Depuis PyPI (recommandé)

```bash
pip install gha-generator
```

#### Depuis le code source (développement)

```bash
# Cloner le repository
git clone https://github.com/Juan-Lucas/github-actions-generator.git
cd github-actions-generator

# Installer en mode editable
pip install -e .
```


## Utilisation

### Créer un workflow

```bash
gha-gen create --type <template> --name <nom-projet> [OPTIONS]
```

**Options principales :**
- `--type` : Type de template (data-science, django-api, laravel-api, react-app, fastapi, flask, express, vue, docker, custom)
- `--name` : Nom du projet
- `--python-version` : Version de Python (défaut: 3.11)
- `--php-version` : Version de PHP (défaut: 8.2)
- `--node-version` : Version de Node.js (défaut: 18)
- `--output` : Répertoire de sortie (défaut: .github/workflows)
- `--workflows` : Générer plusieurs workflows d'un coup (ex: ci,deploy,release)
- `--env` : Variables d'environnement personnalisées (ex: --env FOO=bar)
- `--config` : Fichier de configuration YAML (.gha-gen.yml)

**Exemples concrets :**

```bash
# Workflow Data Science
gha-gen create --type data-science --name mon-projet-ml

# Workflow Django avec Python 3.10
gha-gen create --type django-api --name api-backend --python-version 3.10

# Workflow Laravel
gha-gen create --type laravel-api --name laravel-backend

# Workflow React avec Node.js 20
gha-gen create --type react-app --name frontend-app --node-version 20

# Multi-workflows (ci, deploy, release)
gha-gen create --type fastapi --name my-api --workflows ci,deploy,release

# Variables d'environnement personnalisées
gha-gen create --type django-api --name my-django --env SECRET_KEY=xxx --env DEBUG=1

# Utiliser un template personnalisé
gha-gen template create my-custom
gha-gen create --type my-custom --name projet-special

# Générer depuis un fichier de config YAML
gha-gen create --config .gha-gen.yml
```

### Cas d'usage réels

- **Projet Data Science** : automatiser tests, lint, validation notebooks Jupyter
- **API Django** : CI/CD avec migrations, tests, sécurité, PostgreSQL
- **Frontend React** : build, lint, tests, audit sécurité, déploiement
- **API FastAPI** : tests, coverage, build/push Docker, déploiement cloud

### Captures d'écran & GIF

<img src="docs/img/gha-gen-demo.gif" alt="Démo CLI" width="600" />

<img src="docs/img/gha-gen-list-templates.png" alt="Liste templates" width="600" />

> Ajoutez vos propres captures d'écran ou GIF dans le dossier `docs/img/` pour illustrer l'utilisation !



### Autres commandes utiles

```bash
# Lister les templates disponibles (y compris personnalisés)
gha-gen list-templates

# Valider un workflow existant
gha-gen validate --file .github/workflows/ci.yml

# Lint stricte (best practices)
gha-gen lint --file .github/workflows/ci.yml

# Prévisualiser un workflow sans créer de fichier
gha-gen preview --type fastapi --name my-fastapi-app

# Mode interactif (questionnaire CLI)
gha-gen init

# Créer la structure complète d'un projet
gha-gen init-project --name mon-nouveau-projet

# Exporter vers GitLab CI ou CircleCI
gha-gen export --from .github/workflows/ci.yml --to gitlab-ci
gha-gen export --from .github/workflows/ci.yml --to circleci
```



## Templates disponibles

### data-science
Projets Data Science, Machine Learning, Notebooks Jupyter  
**Inclut:** Setup Python, linting (Ruff, Black, Flake8), tests pytest, validation notebooks

### django-api
Applications Django, API Django REST Framework  
**Inclut:** Setup Python, PostgreSQL, migrations Django, tests pytest-django, linting

### laravel-api
Applications Laravel, API PHP  
**Inclut:** Setup PHP, MySQL, Composer, tests PHPUnit, linting PHP CodeSniffer

### react-app
Applications React, Next.js, Node.js frontend  
**Inclut:** Setup Node.js, ESLint, Prettier, tests Jest, build production

### fastapi
Applications FastAPI, API Python asynchrone  
**Inclut:** Setup Python, linting, tests pytest, coverage, build/push Docker, déploiement cloud


## Tests

```bash
# Exécuter les tests unitaires
pytest

# Avec coverage
pytest --cov=gha_generator
```

**69 tests, 84% de couverture**

## Documentation complète

La documentation détaillée (API, guides, exemples avancés) est disponible sur [ReadTheDocs](https://gha-generator.readthedocs.io/) *(à compléter)* ou dans le dossier `docs/` du projet.

Pour contribuer à la doc, voir le guide dans `CONTRIBUTING.md`.

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Installer en mode dev (`pip install -e .`)
4. Développer et tester (`pytest`)
5. Commit (`git commit -m 'feat: nouvelle fonctionnalité'`)
6. Push et ouvrir une Pull Request

## Auteur

Jean-Luc MUPASA KALUNGA

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
