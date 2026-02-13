# Documentation API

## Modules principaux

- `gha_generator.main` : Entrée CLI, commandes principales
- `gha_generator.generator` : Génération de workflows à partir de templates Jinja2
- `gha_generator.config` : Gestion de la configuration globale
- `gha_generator.stats` : Statistiques d’utilisation
- `gha_generator.validators` : Validation et lint des workflows

## Exemple d’utilisation (Python)

```python
from gha_generator.generator import WorkflowGenerator

gen = WorkflowGenerator()
content = gen.render_template(
    gen.load_template("data-science"),
    {"project_name": "demo", "python_version": "3.11"}
)
print(content)
```

---

> Pour plus de détails, consultez le code source ou ouvrez une issue.
