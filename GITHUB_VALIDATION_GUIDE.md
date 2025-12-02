# Instructions de Validation GitHub Actions

Ce guide explique comment valider les workflows générés dans un environnement GitHub Actions réel.

## 🎯 Objectif

Tester l'exécution des workflows générés par `gha-generator` dans l'environnement GitHub Actions pour s'assurer qu'ils fonctionnent correctement en production.

## 📋 Prérequis

- Compte GitHub
- Git installé et configuré
- Repository GitHub créé (peut être public ou privé)
- Projet avec workflow généré par `gha-gen`

## 🚀 Méthode 1 : Via GitHub CLI (Recommandé)

### Installation de GitHub CLI

**Windows (via winget):**
```powershell
winget install --id GitHub.cli
```

**Windows (via Chocolatey):**
```powershell
choco install gh
```

**macOS:**
```bash
brew install gh
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora
sudo dnf install gh
```

### Authentification

```bash
gh auth login
```

Suivre les instructions pour s'authentifier avec GitHub.

### Création et Push du Repository de Test

```bash
# Se placer dans un nouveau projet
mkdir test-gha-project
cd test-gha-project

# Initialiser Git
git init

# Générer un workflow avec gha-gen
gha-gen create --type data-science --name mon-projet --python-version 3.11

# Créer des fichiers de base pour le test
echo "# Test Project" > README.md

# Python project example
cat > main.py << 'EOF'
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    print(hello())
EOF

cat > test_main.py << 'EOF'
from main import hello

def test_hello():
    assert hello() == "Hello, World!"
EOF

cat > requirements.txt << 'EOF'
pytest>=7.4.0
pytest-cov>=4.1.0
ruff>=0.1.0
black>=23.0.0
flake8>=6.1.0
EOF

# Commit
git add .
git commit -m "Initial commit with GitHub Actions workflow"

# Créer le repository et pousser
gh repo create test-gha-project --public --source=. --remote=origin --push
```

### Vérifier l'Exécution

```bash
# Ouvrir la page Actions du repository
gh repo view --web

# Ou voir les workflows en CLI
gh run list
gh run view <run-id>
```

## 🌐 Méthode 2 : Via GitHub Web (Manuel)

### Étape 1 : Créer le Repository sur GitHub.com

1. Aller sur https://github.com/new
2. Remplir les informations :
   - **Repository name:** `test-gha-validation`
   - **Description:** `Test project for GitHub Actions Generator`
   - **Visibility:** Public ou Private
   - Ne pas initialiser avec README, .gitignore, ou licence
3. Cliquer sur **Create repository**

### Étape 2 : Préparer le Projet Local

```bash
# Créer le répertoire
mkdir test-gha-validation
cd test-gha-validation

# Initialiser Git
git init
git branch -M main

# Générer le workflow
gha-gen create --type data-science --name test-project --python-version 3.11

# Créer les fichiers du projet (voir exemples ci-dessus)
# ... créer main.py, test_main.py, requirements.txt, README.md

# Ajouter les fichiers
git add .
git commit -m "Initial commit with GitHub Actions workflow"
```

### Étape 3 : Connecter et Pousser vers GitHub

```bash
# Remplacer YOUR_USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/YOUR_USERNAME/test-gha-validation.git
git push -u origin main
```

### Étape 4 : Vérifier l'Exécution

1. Aller sur votre repository : `https://github.com/YOUR_USERNAME/test-gha-validation`
2. Cliquer sur l'onglet **Actions**
3. Vous devriez voir votre workflow en cours d'exécution ou terminé
4. Cliquer sur le workflow pour voir les détails et logs

## 🧪 Projets de Test par Template

### Data Science

```bash
# Structure minimale
.
├── .github/workflows/ci.yml
├── main.py
├── test_main.py
├── requirements.txt
└── README.md

# requirements.txt
numpy>=1.24.0
pandas>=2.0.0
pytest>=7.4.0
pytest-cov>=4.1.0
ruff>=0.1.0
black>=23.0.0
flake8>=6.1.0
```

### Django API

```bash
# Structure minimale
.
├── .github/workflows/ci.yml
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── README.md

# requirements.txt
django>=4.2.0
djangorestframework>=3.14.0
pytest>=7.4.0
pytest-django>=4.5.0
pytest-cov>=4.1.0
psycopg2-binary>=2.9.0
```

### Laravel API

```bash
# Structure minimale (après composer create-project)
.
├── .github/workflows/ci.yml
├── app/
├── bootstrap/
├── config/
├── database/
├── public/
├── resources/
├── routes/
├── storage/
├── tests/
├── artisan
├── composer.json
├── phpunit.xml
└── README.md
```

### React App

```bash
# Structure minimale (après create-react-app)
.
├── .github/workflows/ci.yml
├── public/
├── src/
│   ├── App.js
│   ├── App.test.js
│   └── index.js
├── package.json
├── package-lock.json
└── README.md

# package.json (scripts requis)
{
  "scripts": {
    "test": "react-scripts test",
    "build": "react-scripts build",
    "lint": "eslint src/",
    "format:check": "prettier --check src/"
  }
}
```

## ✅ Checklist de Vérification

Après le push, vérifier que :

### Dans l'onglet Actions

- [ ] Le workflow se lance automatiquement
- [ ] Le statut initial est "In progress" ou "Queued"
- [ ] Tous les jobs sont visibles
- [ ] Les steps s'exécutent dans l'ordre

### Pour le Job "test"

- [ ] ✅ Checkout repository
- [ ] ✅ Setup Python/PHP/Node (selon le template)
- [ ] ✅ Install dependencies
- [ ] ✅ Linting (Ruff/Black/Flake8 ou ESLint/Prettier ou phpcs)
- [ ] ✅ Run tests
- [ ] ✅ Upload coverage (si configuré)

### Résultat Final

- [ ] Workflow status: ✅ Success (vert)
- [ ] Durée d'exécution < 30 minutes (timeout)
- [ ] Aucune erreur critique
- [ ] Logs détaillés disponibles

## 🔧 Dépannage

### Workflow ne se lance pas

**Causes possibles:**
- Fichier workflow mal placé (doit être dans `.github/workflows/`)
- Syntaxe YAML invalide
- Permissions GitHub Actions désactivées

**Solutions:**
```bash
# Vérifier l'emplacement
ls -la .github/workflows/

# Valider la syntaxe
gha-gen validate --file .github/workflows/ci.yml

# Vérifier dans Settings > Actions > General
# "Allow all actions and reusable workflows" doit être coché
```

### Tests échouent

**Causes possibles:**
- Dependencies manquantes dans requirements.txt/package.json/composer.json
- Chemins incorrects
- Variables d'environnement manquantes

**Solutions:**
```bash
# Tester localement d'abord
pytest  # Pour Python
npm test  # Pour Node.js
./vendor/bin/phpunit  # Pour PHP

# Ajouter les dépendances manquantes
pip freeze > requirements.txt  # Python
npm install --save-dev <package>  # Node.js
composer require --dev <package>  # PHP
```

### Cache ne fonctionne pas

**Vérifier:**
- La version de l'action setup-* est v4
- Le paramètre `cache` est défini (`cache: 'pip'`, `cache: 'npm'`, etc.)
- Le fichier lock existe (package-lock.json, composer.lock, poetry.lock)

### Services containers (PostgreSQL, MySQL) ne démarrent pas

**Vérifier:**
- La syntaxe du service dans le YAML
- Les ports exposés
- Les variables d'environnement (DATABASE_URL, DB_HOST, etc.)
- Les health checks

## 📊 Métriques à Surveiller

Après plusieurs exécutions, analyser :

- **Temps d'exécution moyen** : Devrait être stable
- **Taux de succès** : Devrait être > 95%
- **Cache hit rate** : Devrait améliorer la vitesse
- **Coût** : Minutes GitHub Actions utilisées

## 🎯 Validation Complète

Pour une validation complète, tester :

1. **Push sur main** : ✅ Workflow se lance
2. **Push sur dev** : ✅ Workflow se lance
3. **Pull Request** : ✅ Workflow se lance
4. **Multiple workflows** : ✅ Peuvent coexister
5. **Branch protection** : ✅ Peut exiger status checks

## 📝 Rapport de Validation

Après tests, documenter :

```markdown
## Rapport de Validation GitHub Actions

**Date:** [Date]
**Repository:** [URL]
**Template:** [Type]

### Résultats
- ✅/❌ Workflow lancé automatiquement
- ✅/❌ Tous les jobs passés
- ✅/❌ Tests exécutés avec succès
- ✅/❌ Coverage uploadé
- ✅/❌ Artifacts générés

### Temps d'exécution
- Setup: [X]s
- Dependencies: [X]s
- Linting: [X]s
- Tests: [X]s
- **Total:** [X]min [X]s

### Observations
[Notes et remarques]

### Recommandations
[Améliorations suggérées]
```

## 🔗 Ressources Utiles

- [Documentation GitHub Actions](https://docs.github.com/en/actions)
- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [GitHub Actions Status](https://www.githubstatus.com/)
- [Actions Marketplace](https://github.com/marketplace?type=actions)

---

**Note:** Ce projet a été validé localement avec 69 tests passants (84% coverage). Voir [VALIDATION_REPORT.md](VALIDATION_REPORT.md) pour les détails.
