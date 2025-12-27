import os
from pathlib import Path

# Show environment variable sources
print("=== Checking OpenAI API Key Sources ===\n")

# Show what's in the current environment
current_key = os.getenv("OPENAI_API_KEY")
current_project = os.getenv("OPENAI_PROJECT")

print(f"Current Process Environment:")
print(f"  OPENAI_API_KEY: {(current_key[:20] + '...' + current_key[-6:]) if current_key else '<not set>'}")
print(f"  OPENAI_PROJECT: {current_project or '<not set>'}\n")

# Show Windows environment variables
import subprocess

print(f"Windows User Environment Variables:")
result = subprocess.run(
    ["powershell", "-Command", '[Environment]::GetEnvironmentVariable("OPENAI_API_KEY","User")'],
    capture_output=True, text=True
)
user_key = result.stdout.strip()
print(f"  OPENAI_API_KEY: {(user_key[:20] + '...' + user_key[-6:]) if user_key else '<not set>'}")

result = subprocess.run(
    ["powershell", "-Command", '[Environment]::GetEnvironmentVariable("OPENAI_PROJECT","User")'],
    capture_output=True, text=True
)
user_project = result.stdout.strip()
print(f"  OPENAI_PROJECT: {user_project or '<not set>'}\n")

print(f"Windows System Environment Variables:")
result = subprocess.run(
    ["powershell", "-Command", '[Environment]::GetEnvironmentVariable("OPENAI_API_KEY","Machine")'],
    capture_output=True, text=True
)
system_key = result.stdout.strip()
print(f"  OPENAI_API_KEY: {(system_key[:20] + '...' + system_key[-6:]) if system_key else '<not set>'}")

result = subprocess.run(
    ["powershell", "-Command", '[Environment]::GetEnvironmentVariable("OPENAI_PROJECT","Machine")'],
    capture_output=True, text=True
)
system_project = result.stdout.strip()
print(f"  OPENAI_PROJECT: {system_project or '<not set>'}\n")

# Show .env file
print(f"Project .env file:")
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            if line.startswith("OPENAI"):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    key_name = parts[0]
                    key_value = parts[1].strip()
                    if key_value:
                        display = key_value[:20] + "..." + key_value[-6:] if len(key_value) > 26 else "***"
                        print(f"  {key_name}: {display}")
                    else:
                        print(f"  {key_name}: <empty>")
else:
    print(f"  .env not found at {env_path}")

print("\n=== DIAGNOSIS ===")
if user_key and user_key != (current_key or ""):
    print(f"⚠ WARNING: User-level env var differs from process env!")
    print(f"  Fix: Remove Windows User var: [Environment]::SetEnvironmentVariable('OPENAI_API_KEY',$null,'User')")

if system_key and system_key != (current_key or ""):
    print(f"⚠ WARNING: System-level env var differs from process env!")
    print(f"  Fix: Remove Windows System var (requires admin): [Environment]::SetEnvironmentVariable('OPENAI_API_KEY',$null,'Machine')")

if current_key and current_key.startswith("sk-proj-"):
    if not current_project:
        print(f"⚠ ERROR: Project-scoped key detected but OPENAI_PROJECT not set!")
        print(f"  Fix: Add OPENAI_PROJECT=proj_... to .env or Windows env vars")
    else:
        print(f"✓ Project-scoped key with project set: {current_project}")
elif current_key and current_key.startswith("sk-svcacct-"):
    print(f"✓ Service account key loaded (no project needed)")
elif current_key:
    print(f"✓ User API key loaded")
else:
    print(f"✗ No API key found!")
