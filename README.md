# GitHub Actions Generator

> Un outil CLI puissant pour générer des workflows GitHub Actions personnalisés et standardisés

## 🎯 Description

GitHub Actions Generator est un outil en ligne de commande qui automatise la création de fichiers de configuration YAML pour GitHub Actions. Il permet de standardiser et d'accélérer la mise en place des pipelines CI/CD pour différents environnements techniques (Data Science, Django, Laravel, React, etc.).

## ✨ Fonctionnalités

- **Génération automatique** de workflows GitHub Actions
- **Templates pré-configurés** pour différentes stacks technologiques
- **Paramétrage dynamique** (nom de projet, versions, dépendances)
- **Configuration standardisée** incluant linting, tests et déploiement
- **Interface CLI intuitive** avec Click
- **Validation YAML** automatique

## 📦 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (pour le développement)

### Installation en mode développement

```bash
# Cloner le repository
git clone https://github.com/Juan-Lucas/github-actions-generator.git
cd github-actions-generator

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer en mode éditable avec les dépendances
pip install -e .
```

### Installation depuis PyPI (à venir)

```bash
pip install gha-generator
```

### Vérification de l'installation

```bash
# Vérifier la version installée
gha-gen --version

# Afficher l'aide
gha-gen --help
```

## 🚀 Utilisation

### Commandes principales

#### 1. Créer un nouveau workflow

```bash
gha-gen create --type <template> --name <nom-projet> [OPTIONS]
```

**Options disponibles:**
- `--type` : Type de template (data-science, django-api, laravel-api, react-app) *[obligatoire]*
- `--name` : Nom du projet *[obligatoire]*
- `--python-version` : Version de Python (par défaut: 3.11)
- `--php-version` : Version de PHP (par défaut: 8.2)
- `--node-version` : Version de Node.js (par défaut: 18)
- `--output` : Répertoire de sortie (par défaut: .github/workflows)

**Exemples:**

```bash
# Workflow Data Science avec Python 3.11
gha-gen create --type data-science --name mon-projet-ml

# Workflow Django avec version Python personnalisée
gha-gen create --type django-api --name api-backend --python-version 3.10

# Workflow Laravel avec PHP 8.2
gha-gen create --type laravel-api --name laravel-backend --php-version 8.2

# Workflow React avec Node.js 20 et sortie personnalisée
gha-gen create --type react-app --name frontend-app --node-version 20 --output workflows
```

#### 2. Lister les templates disponibles

```bash
gha-gen list-templates
```

Affiche tous les templates disponibles avec leurs descriptions.

#### 3. Valider un workflow existant

```bash
gha-gen validate --file <chemin-vers-workflow.yml>
```

**Exemple:**
```bash
gha-gen validate --file .github/workflows/ci.yml
```

Vérifie la syntaxe YAML et la validité du fichier de workflow.

## 📋 Templates disponibles

### 🐍 data-science
**Pour:** Projets Data Science, Machine Learning, Notebooks Jupyter

**Inclut:**
- Setup Python avec cache pip automatique
- Installation des dépendances depuis requirements.txt
- Linting avec Ruff, Black et Flake8
- Tests avec pytest et génération de coverage
- Validation des notebooks Jupyter (syntaxe et exécution)
- Artifacts de test et rapports de coverage

**Variables:**
- `project_name` : Nom du projet
- `python_version` : Version Python (défaut: 3.11)

---

### 🌐 django-api
**Pour:** Applications Django, API Django REST Framework

**Inclut:**
- Setup Python avec cache pip
- Service PostgreSQL pour tests
- Vérification des migrations Django
- Tests avec pytest-django et coverage
- Linting et formatage
- Job de déploiement optionnel

**Variables:**
- `project_name` : Nom du projet
- `python_version` : Version Python (défaut: 3.11)

---

### ⚡ laravel-api
**Pour:** Applications Laravel, API PHP

**Inclut:**
- Setup PHP avec extensions
- Service MySQL pour tests
- Installation des dépendances via Composer
- Tests PHPUnit avec coverage
- Linting PHP CodeSniffer
- Audit de sécurité composer
- Job de déploiement optionnel

**Variables:**
- `project_name` : Nom du projet
- `php_version` : Version PHP (défaut: 8.2)

---

### ⚛️ react-app
**Pour:** Applications React, Next.js, applications Node.js frontend

**Inclut:**
- Setup Node.js avec cache npm
- Installation des dépendances
- Linting avec ESLint et Prettier
- Tests avec Jest et coverage
- Build de production
- Analyse de la taille du bundle
- Upload des artifacts de build

**Variables:**
- `project_name` : Nom du projet
- `node_version` : Version Node.js (défaut: 18)

## 🛠️ Structure du projet

```
github-actions-generator/
├── gha_generator/          # Code source
│   ├── __init__.py
│   ├── main.py            # Point d'entrée CLI
│   ├── generator.py       # Logique de génération
│   ├── utils.py           # Fonctions utilitaires
│   └── templates/         # Templates YAML
│       ├── base.yml
│       ├── data-science.yml
│       ├── django-api.yml
│       ├── laravel-api.yml
│       └── react-app.yml
├── tests/                 # Tests unitaires
├── requirements.txt       # Dépendances
├── setup.py              # Configuration du package
└── README.md             # Documentation
```

## 🧪 Tests

Le projet inclut une suite complète de tests (69 tests, 84% de couverture).

```bash
# Exécuter tous les tests
pytest

# Exécuter avec coverage détaillée
pytest --cov=gha_generator --cov-report=html --cov-report=term

# Tests avec sortie détaillée
pytest -v

# Tests spécifiques par fichier
pytest tests/test_generator.py
pytest tests/test_cli.py
pytest tests/test_utils.py

# Tests d'intégration uniquement
pytest tests/test_integration.py

# Lancer les outils de qualité de code
ruff check gha_generator/
black --check gha_generator/
flake8 gha_generator/
```

### Structure des tests

- **test_generator.py** : Tests de la classe WorkflowGenerator (39 tests)
- **test_cli.py** : Tests des commandes CLI avec Click (18 tests)
- **test_utils.py** : Tests des fonctions utilitaires (20 tests)
- **test_integration.py** : Tests end-to-end complets (12 tests)

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

### Workflow de contribution

1. **Fork** le projet sur GitHub
2. **Cloner** votre fork localement
   ```bash
   git clone https://github.com/votre-username/github-actions-generator.git
   cd github-actions-generator
   ```
3. **Créer une branche** pour votre fonctionnalité
   ```bash
   git checkout -b feature/nouvelle-fonctionnalite
   ```
4. **Installer** en mode développement
   ```bash
   pip install -e .
   pip install -r requirements.txt
   ```
5. **Développer** votre fonctionnalité avec les tests associés
6. **Vérifier** la qualité du code
   ```bash
   pytest
   ruff check gha_generator/
   black gha_generator/
   ```
7. **Commit** vos changements
   ```bash
   git commit -m 'feat: ajout nouvelle fonctionnalité'
   ```
8. **Push** vers votre fork
   ```bash
   git push origin feature/nouvelle-fonctionnalite
   ```
9. **Ouvrir une Pull Request** sur le repository principal

### Guidelines de contribution

- **Code style** : Suivre PEP 8, utiliser Black et Ruff
- **Tests** : Ajouter des tests pour toute nouvelle fonctionnalité
- **Documentation** : Mettre à jour le README si nécessaire
- **Commits** : Utiliser des messages clairs (Conventional Commits recommandé)
- **Coverage** : Maintenir le taux de couverture au-dessus de 80%

## 📝 Variables et personnalisation

### Variables de template

Chaque template utilise le moteur Jinja2 pour la génération dynamique :

| Variable | Type | Templates | Défaut | Description |
|----------|------|-----------|--------|-------------|
| `project_name` | string | Tous | *requis* | Nom du projet (utilisé dans les jobs) |
| `python_version` | string | data-science, django-api | 3.11 | Version de Python (ex: 3.9, 3.10, 3.11) |
| `php_version` | string | laravel-api | 8.2 | Version de PHP (ex: 8.1, 8.2, 8.3) |
| `node_version` | string | react-app | 18 | Version de Node.js (ex: 16, 18, 20) |

### Personnalisation avancée

Les workflows générés peuvent être personnalisés après création :

1. **Ajouter des étapes** : Insérer de nouveaux steps dans les jobs existants
2. **Modifier les triggers** : Changer les événements `on` (push, pull_request, schedule)
3. **Ajuster les permissions** : Modifier les permissions GitHub selon vos besoins
4. **Configurer les secrets** : Ajouter des variables d'environnement sensibles via GitHub Secrets
5. **Activer/désactiver des jobs** : Commenter ou supprimer des jobs non nécessaires

### Structure d'un workflow généré

```yaml
name: CI - <project_name>
on: [push, pull_request]
permissions: read-all

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - name: Setup environment
        # Configuration spécifique au template
      - name: Install dependencies
        # Installation des dépendances
      - name: Run tests
        # Exécution des tests
```

## � Dépendances

### Dépendances de production

- **click** ≥ 8.1.0 : Framework CLI avec décorateurs
- **jinja2** ≥ 3.1.0 : Moteur de templates pour génération YAML
- **pyyaml** ≥ 6.0 : Parser et validateur YAML

### Dépendances de développement

- **pytest** ≥ 7.4.0 : Framework de tests
- **pytest-cov** ≥ 4.1.0 : Plugin coverage pour pytest
- **ruff** ≥ 0.1.0 : Linter Python ultra-rapide
- **black** ≥ 23.0.0 : Formateur de code Python
- **flake8** ≥ 6.1.0 : Linter PEP 8

## ❓ FAQ

### Comment ajouter un nouveau template ?

1. Créer un fichier `.yml` dans `gha_generator/templates/`
2. Utiliser les variables Jinja2 : `{{ project_name }}`, `{{ python_version }}`, etc.
3. Ajouter des tests dans `tests/test_integration.py`
4. Mettre à jour la documentation

### Puis-je utiliser cet outil pour des projets existants ?

Oui ! Utilisez l'option `--output` pour générer le workflow dans un répertoire personnalisé, puis copiez-le manuellement dans `.github/workflows/`.

### Les workflows générés fonctionnent-ils immédiatement ?

Les templates sont pré-configurés pour fonctionner avec des structures de projet standards. Vous devrez peut-être ajuster :
- Les chemins vers les fichiers de dépendances
- Les commandes de test spécifiques
- Les variables d'environnement

### Comment contribuer un nouveau template ?

Consultez la section [Contribution](#-contribution) et ouvrez une Pull Request avec votre template et les tests associés.

## 🗺️ Roadmap

- [x] Templates de base (Python, PHP, Node.js)
- [x] CLI complète avec Click
- [x] Tests unitaires et d'intégration (84% coverage)
- [x] CI/CD avec GitHub Actions
- [ ] Support de templates additionnels (Flutter, Go, Rust, etc.)
- [ ] Génération de multiples workflows par projet
- [ ] Commande `update` pour mise à jour de workflows existants
- [ ] Intégration d'un assistant IA pour suggestions contextuelles
- [ ] Interface graphique (GUI)
- [ ] Publication sur PyPI

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**GitHub Actions Generator** - Créé avec ❤️ pour automatiser et standardiser les workflows CI/CD

Repository : [https://github.com/Juan-Lucas/github-actions-generator](https://github.com/Juan-Lucas/github-actions-generator)

## 🙏 Remerciements

- **GitHub Actions** pour leur plateforme d'automatisation puissante
- **Click**, **Jinja2** et **PyYAML** pour les excellentes bibliothèques Python
- La **communauté Python** pour les outils de qualité de code (Ruff, Black, pytest)
