# GitHub Actions Generator

[![PyPI version](https://badge.fury.io/py/gha-generator.svg)](https://badge.fury.io/py/gha-generator)
[![Python](https://img.shields.io/pypi/pyversions/gha-generator.svg)](https://pypi.org/project/gha-generator/)
[![License](https://img.shields.io/pypi/l/gha-generator.svg)](https://github.com/Juan-Lucas/github-actions-generator/blob/main/LICENSE)
[![Downloads](https://pepy.tech/badge/gha-generator)](https://pepy.tech/project/gha-generator)

Un outil CLI pour générer des workflows GitHub Actions personnalisés et standardisés.

## Description

GitHub Actions Generator automatise la création de fichiers YAML pour GitHub Actions. Il permet de standardiser et d'accélérer la mise en place des pipelines CI/CD pour différents environnements techniques (Data Science, Django, Laravel, React).

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip

### Installation

```bash
# Cloner le repository
git clone https://github.com/Juan-Lucas/github-actions-generator.git
cd github-actions-generator

# Installer
pip install -e .
```

## Utilisation

### Créer un workflow

```bash
gha-gen create --type <template> --name <nom-projet> [OPTIONS]
```

**Options:**
- `--type` : Type de template (data-science, django-api, laravel-api, react-app)
- `--name` : Nom du projet
- `--python-version` : Version de Python (défaut: 3.11)
- `--php-version` : Version de PHP (défaut: 8.2)
- `--node-version` : Version de Node.js (défaut: 18)
- `--output` : Répertoire de sortie (défaut: .github/workflows)

**Exemples:**

```bash
# Workflow Data Science
gha-gen create --type data-science --name mon-projet-ml

# Workflow Django avec Python 3.10
gha-gen create --type django-api --name api-backend --python-version 3.10

# Workflow Laravel
gha-gen create --type laravel-api --name laravel-backend

# Workflow React avec Node.js 20
gha-gen create --type react-app --name frontend-app --node-version 20
```

### Autres commandes

```bash
# Lister les templates disponibles
gha-gen list-templates

# Valider un workflow existant
gha-gen validate --file .github/workflows/ci.yml
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

## Tests

```bash
# Exécuter les tests
pytest

# Avec coverage
pytest --cov=gha_generator
```

**69 tests, 84% de couverture**

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Installer en mode dev (`pip install -e .`)
4. Développer et tester (`pytest`)
5. Commit (`git commit -m 'feat: nouvelle fonctionnalité'`)
6. Push et ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

<table>
  <tr>
    <td><img src="https://github.com/Juan-Lucas.png" width="80" style="border-radius: 50%;"></td>
    <td>
      <strong>Jean-Luc Mupasa</strong><br>
      <a href="https://github.com/Juan-Lucas">@Juan-Lucas</a>
    </td>
  </tr>
</table>
