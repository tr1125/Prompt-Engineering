from typing import Dict


def run_dry_run(command: str) -> Dict:
    return {"status": "dry-run", "output": f"Would run: {command}"}
