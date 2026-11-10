#!/usr/bin/env python3
"""Validate published realm discovery and SAML metadata; no login claims."""
import json
from urllib.request import urlopen
from xml.etree import ElementTree


def main():
    base = "http://127.0.0.1:8080/realms/enterprise-corp"
    with urlopen(base + "/.well-known/openid-configuration", timeout=20) as response:
        discovery = json.load(response)
    if discovery.get("issuer") != base or not discovery.get("authorization_endpoint"):
        raise SystemExit("OIDC discovery validation failed")
    with urlopen(base + "/protocol/saml/descriptor", timeout=20) as response:
        root = ElementTree.fromstring(response.read())
    if not root.tag.endswith("EntityDescriptor"):
        raise SystemExit("SAML metadata validation failed")
    print("OIDC discovery and SAML metadata verified (full SP login not exercised).")


if __name__ == "__main__":
    main()
