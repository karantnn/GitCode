import os
import sys

# Prefer .env in project root regardless of CWD
from pathlib import Path
try:
    from dotenv import load_dotenv, find_dotenv
except Exception:
    load_dotenv = None
    find_dotenv = None

project_root = Path(__file__).resolve().parents[1]

if load_dotenv and find_dotenv:
    # Try exact project root first
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        # Fallback search upwards; usecwd=False avoids trapping in external CWD
        found = find_dotenv(usecwd=False)
        if found:
            load_dotenv(found)

key = os.getenv("OPENAI_API_KEY")
project = os.getenv("OPENAI_PROJECT")
org = os.getenv("OPENAI_ORG_ID") or os.getenv("OPENAI_ORGANIZATION")

print("Environment:")
print("  OPENAI_API_KEY:", (key[:10] + "..." + key[-6:]) if key else "<missing>")
print("  OPENAI_PROJECT:", project or "<unset>")
print("  OPENAI_ORG_ID:", org or "<unset>")

# Try a simple models list call via official client
try:
    from openai import OpenAI
except Exception as e:
    print("OpenAI client import failed:", e)
    print("Hint: install 'openai' in your venv: pip install openai")
    sys.exit(2)

client_kwargs = {}
if project:
    client_kwargs["project"] = project
if org:
    client_kwargs["organization"] = org

client = OpenAI(**client_kwargs)

print("\nChecking access to /models...")
try:
    models = client.models.list()
    count = len(getattr(models, "data", []) or [])
    print(f"  Success: models listed (count={count}). Key appears valid.")
    # Show a couple of model IDs for sanity
    for m in (getattr(models, "data", []) or [])[:3]:
        print("   -", getattr(m, "id", "<unknown>"))
    sys.exit(0)
except Exception as e:
    print("  Error during models list:")
    print("  ", e)
    # Common remediation notes
    print("\nRemediation:")
    print("  - Ensure OPENAI_API_KEY is a valid active key (starts with 'sk-').")
    print("  - If using project-scoped keys ('sk-proj-...'), also set OPENAI_PROJECT=proj_... and update to latest 'openai' library.")
    print("  - Remove quotes and trailing spaces from values in .env.")
    print("  - Regenerate a fresh key at https://platform.openai.com/account/api-keys and update .env.")
    sys.exit(1)
