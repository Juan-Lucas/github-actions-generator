# Guide utilisateur

## Installation

```bash
pip install gha-generator
```

## Commandes principales

- `gha-gen create` : Générer un workflow
- `gha-gen list-templates` : Lister les templates
- `gha-gen validate` : Valider un workflow
- `gha-gen preview` : Prévisualiser un workflow
- `gha-gen init` : Mode interactif
- `gha-gen export` : Exporter vers GitLab CI/CircleCI

## Exemples

```bash
# Data Science
gha-gen create --type data-science --name projet-ml

# Multi-workflows
gha-gen create --type fastapi --name my-api --workflows ci,deploy

# Template personnalisé
gha-gen template create my-custom
gha-gen create --type my-custom --name projet-special
```

## FAQ

- **Où trouver les templates ?**
  - Utilisez `gha-gen list-templates` ou consultez le dossier `gha_generator/templates/`.
- **Comment contribuer ?**
  - Voir le fichier CONTRIBUTING.md du projet.
