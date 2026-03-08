import os
import shlex
from typing import Dict, List


FORBIDDEN = {"rm", "del", "shutdown", "format", "mkfs", "dd", ":(){:|:&};:"}
RISKY_FLAGS = {"-rf", "/s", "/q"}


def _tokenize(command: str) -> List[str]:
    try:
        posix = os.name != "nt"
        return shlex.split(command, posix=posix)
    except Exception:
        return command.split()


def validate_command(command: str) -> Dict:
    """Validate a proposed shell command.

    Returns a dict with keys: status (safe|forbidden|requires_confirmation|unknown), reasons (list).
    """
    reasons = []
    if not command or not command.strip():
        return {"status": "forbidden", "reasons": ["empty_command"]}

    toks = _tokenize(command)
    if not toks:
        return {"status": "unknown", "reasons": ["could_not_tokenize"]}

    cmd = toks[0].lower()

    # detect forbidden commands
    for f in FORBIDDEN:
        if cmd == f or (f in cmd):
            reasons.append(f"forbidden_command:{f}")

    # detect risky flags
    for flag in RISKY_FLAGS:
        if flag in command:
            reasons.append(f"risky_flag:{flag}")

    if any(r.startswith("forbidden_command") for r in reasons):
        return {"status": "forbidden", "reasons": reasons}

    if reasons:
        return {"status": "requires_confirmation", "reasons": reasons}

    return {"status": "safe", "reasons": []}
