#!/usr/bin/env python3
"""Generate local-only lab credentials without overwriting an existing file."""
import os
import secrets
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "docker-compose" / ".env"
with path.open("x", encoding="utf-8") as output:
    os.chmod(path, 0o600)
    for key in ("DB_PASSWORD", "LDAP_ADMIN_PASSWORD", "KEYCLOAK_ADMIN_PASSWORD"):
        output.write(f"{key}={secrets.token_urlsafe(32)}\n")
print(f"Generated {path}; keep it outside version control.")
