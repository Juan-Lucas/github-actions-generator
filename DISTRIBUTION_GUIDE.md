# Guide de Distribution - GitHub Actions Generator

Ce document décrit le processus de packaging et de distribution du projet.

## 📦 Création de la Distribution

### Prérequis

```bash
pip install setuptools>=68.0.0 wheel>=0.41.0 build>=1.0.0 twine>=4.0.0
```

### Processus de Build

#### 1. Nettoyer les builds précédents

```bash
# Windows PowerShell
if (Test-Path dist) { Remove-Item -Recurse -Force dist }
if (Test-Path build) { Remove-Item -Recurse -Force build }
if (Test-Path gha_generator.egg-info) { Remove-Item -Recurse -Force gha_generator.egg-info }

# Linux/macOS
rm -rf dist/ build/ gha_generator.egg-info/
```

#### 2. Créer les distributions

```bash
python setup.py sdist bdist_wheel
```

Cette commande crée :
- **Source distribution** : `dist/gha_generator-0.1.0.tar.gz`
- **Wheel distribution** : `dist/gha_generator-0.1.0-py3-none-any.whl`

#### 3. Vérifier les distributions

```bash
python -m twine check dist/*
```

**Résultat attendu :**
```
Checking dist/gha_generator-0.1.0-py3-none-any.whl: PASSED
Checking dist/gha_generator-0.1.0.tar.gz: PASSED
```

## 🧪 Test de la Distribution

### Installation depuis le Wheel

```bash
# Créer un environnement virtuel
python -m venv test_env

# Activer l'environnement
# Windows
.\test_env\Scripts\activate
# Linux/macOS
source test_env/bin/activate

# Installer depuis le wheel
pip install dist/gha_generator-0.1.0-py3-none-any.whl

# Tester la commande
gha-gen --version
gha-gen list-templates
gha-gen create --type data-science --name test --python-version 3.11

# Désactiver et nettoyer
deactivate
rm -rf test_env  # ou Remove-Item sur Windows
```

### Vérifications Essentielles

- [x] ✅ Version affichée correctement : `0.1.0`
- [x] ✅ Commande `gha-gen` accessible
- [x] ✅ Tous les templates disponibles (4)
- [x] ✅ Génération de workflow fonctionnelle
- [x] ✅ Validation YAML fonctionnelle
- [x] ✅ Tous les fichiers template inclus dans le wheel

## 📝 Contenu de la Distribution

### Fichiers inclus (via MANIFEST.in)

```
gha_generator-0.1.0/
├── LICENSE                          # Licence MIT
├── README.md                        # Documentation principale
├── requirements.txt                 # Dépendances
├── setup.py                         # Configuration du package
├── pyproject.toml                   # Configuration moderne
├── MANIFEST.in                      # Règles d'inclusion
├── gha_generator/
│   ├── __init__.py                  # Module principal
│   ├── main.py                      # CLI
│   ├── generator.py                 # Logique de génération
│   ├── utils.py                     # Utilitaires
│   └── templates/
│       ├── __init__.py
│       ├── base.yml
│       ├── data-science.yml
│       ├── django-api.yml
│       ├── laravel-api.yml
│       └── react-app.yml
└── gha_generator.egg-info/          # Métadonnées du package
```

### Fichiers exclus (via .gitignore et MANIFEST.in)

- `tests/` : Tests non nécessaires dans la distribution
- `.github/` : CI/CD interne
- `__pycache__/`, `*.pyc` : Bytecode Python
- `.vscode/`, `.idea/` : Configuration IDE
- `htmlcov/` : Rapports de coverage

## 🚀 Publication sur PyPI

### Test PyPI (Recommandé en premier)

```bash
# S'enregistrer sur TestPyPI : https://test.pypi.org/account/register/

# Upload vers TestPyPI
python -m twine upload --repository testpypi dist/*

# Installer depuis TestPyPI pour tester
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple gha-generator

# Tester l'installation
gha-gen --version
```

### PyPI Production

```bash
# S'enregistrer sur PyPI : https://pypi.org/account/register/

# Configuration de l'authentification
# Méthode 1 : API Token (recommandé)
# Créer un token sur https://pypi.org/manage/account/token/
# Utiliser __token__ comme username et le token comme password

# Méthode 2 : Fichier .pypirc
# Créer ~/.pypirc (Linux/macOS) ou %USERPROFILE%\.pypirc (Windows)
# [pypi]
# username = __token__
# password = <your-token>

# Upload vers PyPI
python -m twine upload dist/*

# Vérifier sur PyPI
# https://pypi.org/project/gha-generator/

# Installer depuis PyPI
pip install gha-generator
```

## 🏷️ Gestion des Versions

### Créer un Tag Git

```bash
# Créer le tag v0.1.0
git tag -a v0.1.0 -m "Release version 0.1.0

- CLI complète avec commandes create, list-templates, validate
- 4 templates : data-science, django-api, laravel-api, react-app
- 69 tests avec 84% coverage
- Documentation complète
- Validation GitHub Actions"

# Pousser le tag vers GitHub
git push origin v0.1.0

# Créer une release GitHub
# Via GitHub CLI
gh release create v0.1.0 \
  --title "v0.1.0 - Initial Release" \
  --notes "First stable release of GitHub Actions Generator" \
  dist/gha_generator-0.1.0.tar.gz \
  dist/gha_generator-0.1.0-py3-none-any.whl

# Ou manuellement sur GitHub :
# https://github.com/<username>/github-actions-generator/releases/new
```

### Mise à Jour de Version

Pour les versions futures :

1. **Modifier la version** dans `gha_generator/__init__.py` et `setup.py`
2. **Mettre à jour** le changelog/README
3. **Reconstruire** : `python setup.py sdist bdist_wheel`
4. **Vérifier** : `python -m twine check dist/*`
5. **Créer le tag** : `git tag -a v0.2.0 -m "Release v0.2.0"`
6. **Publier** : `python -m twine upload dist/*`

## 📊 Statistiques de Distribution

### Taille des Fichiers

```
dist/gha_generator-0.1.0.tar.gz           : ~20 KB (source)
dist/gha_generator-0.1.0-py3-none-any.whl : ~18 KB (wheel)
```

### Dépendances Runtime

- `click>=8.1.0` : Framework CLI
- `jinja2>=3.1.0` : Moteur de templates
- `pyyaml>=6.0` : Parser YAML

Total des dépendances (avec sous-dépendances) : ~5-6 packages

### Compatibilité

- **Python** : ≥ 3.8
- **OS** : Windows, Linux, macOS
- **Architecture** : Pure Python (py3-none-any)

## 🔒 Sécurité

### Vérification de Signature

```bash
# Générer une signature GPG (optionnel)
gpg --detach-sign -a dist/gha_generator-0.1.0.tar.gz

# Vérifier la signature
gpg --verify dist/gha_generator-0.1.0.tar.gz.asc dist/gha_generator-0.1.0.tar.gz
```

### Checksum

```bash
# Générer checksums
# Windows PowerShell
Get-FileHash dist/gha_generator-0.1.0-py3-none-any.whl -Algorithm SHA256
Get-FileHash dist/gha_generator-0.1.0.tar.gz -Algorithm SHA256

# Linux/macOS
sha256sum dist/*
```

## 📚 Ressources

- [Python Packaging Guide](https://packaging.python.org/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [PyPI Publishing Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Semantic Versioning](https://semver.org/)

## ✅ Checklist de Publication

Avant de publier sur PyPI :

- [x] Tests passent à 100% (69/69)
- [x] Coverage ≥ 80% (84%)
- [x] Documentation README complète
- [x] LICENCE incluse (MIT)
- [x] Changelog/Release notes préparés
- [x] Version correcte dans __init__.py et setup.py
- [x] Distribution construite (sdist + wheel)
- [x] Twine check réussi
- [x] Installation depuis wheel testée
- [x] Fonctionnalités validées
- [x] Tag Git créé
- [ ] Publication sur TestPyPI (recommandé)
- [ ] Publication sur PyPI
- [ ] Release GitHub créée

---

**Note** : Les distributions sont créées localement mais ne sont pas versionnées dans Git (exclus via .gitignore). Elles sont disponibles dans le dossier `dist/` après la construction.
