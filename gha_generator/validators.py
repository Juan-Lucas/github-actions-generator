from pathlib import Path
import yaml

def validate_strict(workflow_path: Path) -> tuple[bool, list[str]]:
    """Validation stricte d'un workflow GitHub Actions (best practices)."""
    issues = []
    try:
        with open(workflow_path, encoding="utf-8") as f:
            workflow = yaml.safe_load(f)
    except Exception as e:
        return False, [f"Erreur de lecture du fichier : {str(e)}"]

    jobs = workflow.get("jobs", {})
    for job_name, job in jobs.items():
        # Vérifie la présence de permissions explicites
        if "permissions" not in job:
            issues.append(f"[{job_name}] Permissions non définies (ajoutez 'permissions: read-all' ou plus restrictif)")
        # Vérifie la présence d'un timeout
        if "timeout-minutes" not in job:
            issues.append(f"[{job_name}] timeout-minutes manquant (ex: 30)")
        # Vérifie que chaque action utilisée est versionnée
        for step in job.get("steps", []):
            if "uses" in step:
                action = step["uses"]
                if "@v" not in action and "@main" not in action and "@master" not in action:
                    issues.append(f"[{job_name}] Action sans version : {action}")
    return len(issues) == 0, issues
