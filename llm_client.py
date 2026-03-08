import os
from typing import Dict

# Load .env if present so GOOGLE_API_KEY set there becomes available at runtime
try:
    from dotenv import load_dotenv

    # try package-level .env first (CLIByAI/.env), then project root
    pkg_env = os.path.join(os.path.dirname(__file__), ".env")
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    proj_env = os.path.join(project_root, ".env")

    # load both if present; do not override existing env vars
    if os.path.exists(pkg_env):
        load_dotenv(pkg_env, override=True)
    if os.path.exists(proj_env):
        load_dotenv(proj_env, override=True)
    # final attempt: generic load (will read from current working dir)
    load_dotenv(override=True)
except Exception:
    pass


def generate_command(instruction: str, prompt_text: str = "") -> Dict:
    """Call Google GenAI to produce a CLI command. Returns structured dict.

    Behavior:
    - If `GOOGLE_API_KEY` is not set, returns an error dict (no mock).
    - Tries several genai call styles and parses the raw response to extract a command.
    - Logs the raw response to `CLIByAI/logs/genai_raw.txt` for debugging.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"command": "", "explanation": "No GOOGLE_API_KEY set.", "safety": {"status": "error", "detail": "no_api_key"}}

    prompt = (prompt_text + "\n\n" if prompt_text else "") + instruction

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        config = types.GenerateContentConfig(
            system_instruction=prompt_text if prompt_text else None,
        )
        resp = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            #model="gemini-2.5-flash",
            contents=instruction,
            config=config,
        )
        text = resp.text

        # Save raw response for debugging
        try:
            logs_dir = os.path.join(os.path.dirname(__file__), "logs")
            os.makedirs(logs_dir, exist_ok=True)
            with open(os.path.join(logs_dir, "genai_raw.txt"), "a", encoding="utf-8") as f:
                f.write("=== PROMPT ===\n" + prompt + "\n=== RAW RESPONSE ===\n" + str(text) + "\n\n")
        except Exception:
            pass

        return {"command": str(text).strip()}

    except Exception as e:
        return {"command": "", "explanation": f"LLM error: {e}"}
