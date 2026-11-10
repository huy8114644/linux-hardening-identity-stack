#!/usr/bin/env python3
"""Idempotently configure a read-only LDAP federation in the local Keycloak lab."""
import argparse
import json
import os
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

REALM = "enterprise-corp"
COMPONENT_TYPE = "org.keycloak.storage.UserStorageProvider"


def federation(realm_id: str, password: str) -> dict:
    return {
        "name": "enterprise-ldap",
        "providerId": "ldap",
        "providerType": COMPONENT_TYPE,
        "parentId": realm_id,
        "config": {
            "enabled": ["true"],
            "priority": ["0"],
            "vendor": ["other"],
            "connectionUrl": ["ldap://openldap:389"],
            "usersDn": ["ou=people,dc=enterprise,dc=internal"],
            "bindDn": ["cn=admin,dc=enterprise,dc=internal"],
            "bindCredential": [password],
            "authType": ["simple"],
            "editMode": ["READ_ONLY"],
            "importEnabled": ["true"],
            "syncRegistrations": ["false"],
            "usernameLDAPAttribute": ["uid"],
            "uuidLDAPAttribute": ["entryUUID"],
            "rdnLDAPAttribute": ["uid"],
            "userObjectClasses": ["inetOrgPerson, organizationalPerson"],
            "searchScope": ["1"],
            "pagination": ["true"],
            "connectionTimeout": ["5000"],
            "readTimeout": ["5000"],
        },
    }


def reconcile(base: str, admin_password: str, ldap_password: str) -> str:
    parsed = urlsplit(base)
    if parsed.scheme != "http" or parsed.hostname not in ("127.0.0.1", "localhost"):
        raise ValueError("This lab bootstrap accepts loopback HTTP only; use TLS for production.")

    def request(path: str, method: str = "GET", data=None, token=None):
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if data is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(data).encode()
        with urlopen(Request(base + path, data=data, method=method, headers=headers), timeout=20) as response:
            body = response.read()
            return json.loads(body) if body else None

    credentials = urlencode({
        "grant_type": "password", "client_id": "admin-cli",
        "username": "admin", "password": admin_password,
    }).encode()
    with urlopen(Request(
        base + "/realms/master/protocol/openid-connect/token",
        data=credentials, headers={"Content-Type": "application/x-www-form-urlencoded"},
    ), timeout=20) as response:
        token = json.load(response)["access_token"]
    realm = request(f"/admin/realms/{REALM}", token=token)
    path = f"/admin/realms/{REALM}/components"
    components = request(path + "?" + urlencode({"type": COMPONENT_TYPE}), token=token)
    existing = next((item for item in components if item["name"] == "enterprise-ldap"), None)
    desired = federation(realm["id"], ldap_password)
    if existing:
        desired["id"] = existing["id"]
        request(path + "/" + existing["id"], method="PUT", data=desired, token=token)
        return "Updated LDAP federation"
    request(path, method="POST", data=desired, token=token)
    return "Created LDAP federation"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8080")
    args = parser.parse_args()
    admin = os.environ.get("KEYCLOAK_ADMIN_PASSWORD")
    ldap = os.environ.get("LDAP_ADMIN_PASSWORD")
    if not admin or not ldap:
        parser.error("Export KEYCLOAK_ADMIN_PASSWORD and LDAP_ADMIN_PASSWORD from local .env.")
    try:
        print(reconcile(args.url.rstrip("/"), admin, ldap))
    except Exception as exc:
        # Deliberately omit response bodies and credentials.
        parser.exit(1, f"Bootstrap failed: {type(exc).__name__}. Check realm availability and credentials.\n")


if __name__ == "__main__":
    main()
