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

### Installation en mode développement

```bash
# Cloner le repository
git clone <votre-repo-url>
cd github-actions-generator

# Installer les dépendances
pip install -r requirements.txt

# Installer en mode éditable
pip install -e .
```

### Installation depuis PyPI (à venir)

```bash
pip install gha-generator
```

## 🚀 Utilisation

### Créer un nouveau workflow

```bash
# Générer un workflow pour un projet Data Science
gha-gen create --type data-science --name mon-projet-ml

# Générer un workflow Django avec version Python spécifique
gha-gen create --type django-api --name api-backend --python-version 3.11

# Générer un workflow Laravel
gha-gen create --type laravel-api --name laravel-backend

# Générer un workflow React
gha-gen create --type react-app --name frontend-app
```

### Lister les templates disponibles

```bash
gha-gen list-templates
```

### Valider un workflow existant

```bash
gha-gen validate --file .github/workflows/ci.yml
```

## 📋 Templates disponibles

| Template | Description | Langage | Outils inclus |
|----------|-------------|---------|---------------|
| `data-science` | Projets Data Science/ML | Python | pytest, flake8, black, notebooks |
| `django-api` | API Django/DRF | Python | pytest, coverage, migrations |
| `laravel-api` | API Laravel | PHP | PHPUnit, phpcs, composer |
| `react-app` | Application React | Node.js | jest, eslint, build |

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

```bash
# Exécuter tous les tests
pytest

# Exécuter avec coverage
pytest --cov=gha_generator

# Tests spécifiques
pytest tests/test_generator.py
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrir une Pull Request

## 📝 Variables de template

Chaque template accepte les variables suivantes :

- `project_name` : Nom du projet
- `python_version` : Version de Python (pour templates Python)
- `php_version` : Version de PHP (pour templates PHP)
- `node_version` : Version de Node.js (pour templates Node)
- `dependencies_file` : Fichier de dépendances (requirements.txt, composer.json, package.json)

## 🗺️ Roadmap

- [ ] Support de templates additionnels (Flutter, Node.js backend, etc.)
- [ ] Génération de multiples workflows par projet
- [ ] Intégration d'un assistant IA pour suggestions contextuelles
- [ ] Interface graphique (GUI)
- [ ] Fonctionnalité de mise à jour de workflows existants

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

Créé avec ❤️ pour automatiser et standardiser les workflows CI/CD

## 🙏 Remerciements

- GitHub Actions pour leur plateforme d'automatisation
- La communauté Python pour les outils exceptionnels
