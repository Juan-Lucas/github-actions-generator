# Plan d'amélioration - GitHub Actions Generator

## 🎯 Améliorations prioritaires (v0.2.0)

### 1. **Nouveaux templates** 
- **FastAPI** : API moderne Python asynchrone
- **Flask** : API Python légère
- **Vue.js** : Framework frontend
- **Express.js** : API Node.js
- **Docker** : Workflow pour build/push d'images

### 2. **Mode interactif**
```bash
gha-gen init  # Mode questions-réponses
# ❓ Type de projet: [1] Data Science [2] Django [3] Laravel [4] React
# ❓ Nom du projet: mon-projet
# ❓ Python version: 3.11
```

### 3. **Configuration file** (`.gha-gen.yml`)
```yaml
project:
  type: django-api
  python_version: "3.11"
workflows:
  - ci
  - deploy
```
Puis : `gha-gen create --config .gha-gen.yml`

### 4. **Commandes supplémentaires**
- `gha-gen update` : Mettre à jour un workflow existant
- `gha-gen preview` : Afficher le YAML sans créer le fichier
- `gha-gen init-project` : Créer structure complète (.github/, tests/, etc.)

---

## 🚀 Fonctionnalités avancées (v0.3.0)

### 5. **Support multi-workflows**
```bash
gha-gen create --type django-api --workflows ci,deploy,release
```
Génère 3 fichiers : `ci.yml`, `deploy.yml`, `release.yml`

### 6. **Variables d'environnement personnalisées**
```bash
gha-gen create --type django-api --env DATABASE_URL=postgres://... --env SECRET_KEY=...
```

### 7. **Templates personnalisés**
```bash
# Créer un template custom
gha-gen template create --name my-custom-workflow

# Utiliser un template custom
gha-gen create --type custom:my-custom-workflow
```

### 8. **Export vers d'autres CI/CD**
```bash
gha-gen export --from ci.yml --to gitlab-ci  # Convertit vers .gitlab-ci.yml
gha-gen export --from ci.yml --to circleci   # Convertit vers .circleci/config.yml
```

---

## 📚 Améliorations documentation (v0.1.1)

### 9. **Installation depuis PyPI**
Mettre à jour README :
```bash
# Installation depuis PyPI
pip install gha-generator

# Installation en mode dev
git clone https://github.com/Juan-Lucas/github-actions-generator.git
cd github-actions-generator
pip install -e .
```

### 10. **Exemples concrets**
- Captures d'écran de workflows générés
- Cas d'usage réels (exemples de projets)
- GIF animé montrant l'utilisation

### 11. **Documentation complète**
- ReadTheDocs ou MkDocs
- API documentation
- Guide de contribution détaillé

---

## 🔧 Améliorations techniques (v0.1.1)

### 12. **Validation avancée**
```bash
gha-gen validate --file ci.yml --strict  # Vérifie best practices
gha-gen lint --file ci.yml               # Analyse de sécurité
```

### 13. **Support secrets GitHub**
```bash
gha-gen secrets list                     # Liste secrets requis
gha-gen secrets check                    # Vérifie si secrets configurés
```

### 14. **Dry-run mode**
```bash
gha-gen create --type django-api --dry-run  # Simule sans créer
```

### 15. **Better error messages**
- Messages d'erreur en français/anglais
- Suggestions de correction
- Lien vers documentation

---

## 🎨 Qualité de vie (v0.1.1)

### 16. **Couleurs et formatage CLI**
- Utiliser `rich` pour output coloré
- Progress bars pour opérations longues
- Tables formatées pour `list-templates`

### 17. **Auto-completion**
```bash
gha-gen completion bash > /etc/bash_completion.d/gha-gen
gha-gen completion zsh > ~/.zsh/completions/_gha-gen
```

### 18. **Configuration globale**
```bash
gha-gen config set python_version 3.11
gha-gen config set default_output .github/workflows
```

---

## 📊 Analytics & Monitoring (v0.2.0)

### 19. **Statistiques d'utilisation**
```bash
gha-gen stats  # Workflows générés, templates les plus utilisés
```

### 20. **Version check**
```bash
gha-gen --check-update  # Vérifie si nouvelle version disponible
```

---

## 🔐 Sécurité (v0.2.0)

### 21. **Scan de sécurité**
- Intégrer `safety` pour vérifier dépendances
- Suggérer versions GitHub Actions à jour
- Détecter secrets hardcodés

### 22. **Best practices enforcement**
- Permissions minimales
- Timeout sur jobs
- Cache dependencies

---

## 🎯 Roadmap suggérée

### **v0.1.1** (Quickfix - cette semaine)
- [ ] Fixer URLs dans setup.py (`yourusername` → `Juan-Lucas`)
- [ ] Ajouter installation PyPI dans README
- [ ] Ajouter commande `--check-update`
- [ ] Améliorer messages d'erreur
- [ ] Template FastAPI

### **v0.2.0** (Features - 2-3 semaines)
- [ ] Nouveaux templates (Flask, Express, Vue.js, Docker)
- [ ] Mode interactif (`gha-gen init`)
- [ ] Commande `preview`
- [ ] Support multi-workflows
- [ ] Validation stricte
- [ ] Couleurs CLI avec `rich`

### **v0.3.0** (Advanced - 1-2 mois)
- [ ] Templates personnalisés
- [ ] Export vers GitLab CI / CircleCI
- [ ] Documentation complète (ReadTheDocs)
- [ ] Auto-completion shell
- [ ] Configuration globale
- [ ] Statistiques d'utilisation

---

## 💡 Priorités immédiates recommandées

1. **Fixer URLs dans setup.py** (5 min)
2. **Ajouter template FastAPI** (1h)
3. **Commande `preview`** (30 min)
4. **Installation PyPI dans README** (10 min)
5. **Améliorer messages d'erreur** (1h)

---

## 📋 Templates à ajouter (détails)

### FastAPI Template
```yaml
name: {{ project_name }} - FastAPI CI/CD
jobs:
  test:
    steps:
      - Setup Python {{ python_version }}
      - Install uvicorn, fastapi, pytest
      - Run pytest with coverage
      - Build Docker image
      - Deploy to cloud
```

### Flask Template
```yaml
name: {{ project_name }} - Flask CI/CD
jobs:
  test:
    steps:
      - Setup Python {{ python_version }}
      - Install Flask dependencies
      - Run pytest
      - Test endpoints
```

### Express.js Template
```yaml
name: {{ project_name }} - Express API CI/CD
jobs:
  test:
    steps:
      - Setup Node.js {{ node_version }}
      - npm install
      - ESLint check
      - Jest tests
      - Build production
```

### Vue.js Template
```yaml
name: {{ project_name }} - Vue.js CI/CD
jobs:
  test:
    steps:
      - Setup Node.js {{ node_version }}
      - npm install
      - Vue CLI lint
      - Unit tests (Vitest/Jest)
      - Build production
      - Deploy to Netlify/Vercel
```

### Docker Template
```yaml
name: {{ project_name }} - Docker Build & Push
jobs:
  build:
    steps:
      - Docker build
      - Docker scan (Trivy)
      - Push to Docker Hub / GHCR
      - Deploy to K8s / AWS ECS
```

---

## 🛠️ Modifications techniques nécessaires

### Pour mode interactif
```python
# gha_generator/interactive.py
import questionary

def interactive_mode():
    project_type = questionary.select(
        "Type de projet ?",
        choices=["Data Science", "Django API", "Laravel API", "React App", "FastAPI"]
    ).ask()
    
    project_name = questionary.text("Nom du projet ?").ask()
    python_version = questionary.text("Version Python ?", default="3.11").ask()
    
    return {
        "type": project_type.lower().replace(" ", "-"),
        "name": project_name,
        "python_version": python_version
    }
```

### Pour commande preview
```python
# Dans main.py
@cli.command()
@click.option("--type", "-t", required=True)
@click.option("--name", "-n", required=True)
def preview(project_type: str, project_name: str):
    """Preview workflow without creating file."""
    generator = WorkflowGenerator()
    template = generator.load_template(project_type)
    content = generator.render_template(template, {
        "project_name": project_name,
        "python_version": "3.11"
    })
    
    click.echo("=" * 50)
    click.echo(content)
    click.echo("=" * 50)
```

### Pour validation stricte
```python
# gha_generator/validators.py
def validate_strict(workflow_path: Path) -> tuple[bool, list[str]]:
    """Validate workflow with best practices."""
    issues = []
    
    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)
    
    # Check permissions
    if "permissions" not in workflow.get("jobs", {}).get("test", {}):
        issues.append("⚠️ Missing explicit permissions")
    
    # Check timeout
    if "timeout-minutes" not in workflow.get("jobs", {}).get("test", {}):
        issues.append("⚠️ Missing job timeout")
    
    # Check actions versions
    for step in workflow.get("jobs", {}).get("test", {}).get("steps", []):
        if "uses" in step:
            action = step["uses"]
            if "@v" not in action and "@main" not in action:
                issues.append(f"⚠️ Action without version: {action}")
    
    return len(issues) == 0, issues
```

---

## 📦 Nouvelles dépendances à ajouter

```txt
# requirements.txt (ajouts)
rich>=13.0.0           # Pour CLI coloré
questionary>=2.0.0     # Pour mode interactif
requests>=2.31.0       # Pour check-update
safety>=3.0.0          # Pour scan sécurité
```

---

## 🎨 Exemple avec Rich

```python
from rich.console import Console
from rich.table import Table

console = Console()

@cli.command()
def list_templates():
    """List all available project templates."""
    generator = WorkflowGenerator()
    templates = generator.list_templates()
    
    table = Table(title="📋 Available Templates")
    table.add_column("Template", style="cyan")
    table.add_column("Description", style="green")
    
    descriptions = {
        "data-science": "Data Science, ML, Jupyter Notebooks",
        "django-api": "Django REST Framework API",
        "laravel-api": "Laravel PHP API",
        "react-app": "React / Next.js Frontend"
    }
    
    for template in templates:
        table.add_row(template, descriptions.get(template, "N/A"))
    
    console.print(table)
```

---

## ✅ Checklist avant release v0.1.1

- [ ] Fixer URLs dans setup.py
- [ ] Mettre à jour README avec installation PyPI
- [ ] Ajouter template FastAPI
- [ ] Implémenter commande `preview`
- [ ] Tester sur Python 3.10, 3.11, 3.12
- [ ] Mettre à jour version → 0.1.1
- [ ] Créer CHANGELOG.md
- [ ] Tester installation : `pip install gha-generator`
- [ ] Build : `python -m build`
- [ ] Upload PyPI : `twine upload dist/*`
- [ ] Git tag : `git tag v0.1.1`
- [ ] GitHub Release

---

## 📝 Notes

- Privilégier fonctionnalités simples et utiles (preview, FastAPI)
- Maintenir compatibilité backward
- Documenter chaque nouvelle feature
- Tests pour chaque ajout (maintenir 80%+ coverage)
- Suivre Semantic Versioning (MAJOR.MINOR.PATCH)
