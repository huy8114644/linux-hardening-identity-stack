# Linux Hardening & Enterprise Identity Stack

A reproducible lab combining an Ansible Linux baseline with Keycloak and OpenLDAP. It demonstrates selected CIS-inspired controls and identity integration patterns. It does **not** certify CIS Level 1/2 compliance or represent an employer deployment.

## Architecture and layout

Ansible applies a reviewed baseline to staging Linux hosts. Keycloak authenticates against a PostgreSQL database and a read-only LDAP federation, exposing OIDC and SAML integration points.

- roles/cis_hardening/: SSH, audit rules, filesystem blacklists, sysctl, optional PAM and UFW/nftables.
- identity/: local Compose stack, realm import, LDAP federation reconciler.
- tests/: offline contract and configuration tests.
- docs/: control coverage, operating procedures, limitations.

## Validate without changing the host

Requires Python 3.11–3.12, Docker with Compose, and Make. Run **make setup**, then **make check** for Ruff, Pytest, Ansible syntax and Compose validation. **make molecule** tests an isolated Ubuntu container, including convergence and idempotence; it requires privileged Docker on a dedicated test machine.

Container tests intentionally skip host kernel, firewall activation and service reloads. Validate those controls on disposable VMs before production use. GitLab integration needs a dedicated runner tagged docker-privileged.

## Review and apply the OS baseline

Edit inventory.ini with a staging host and verify key-based access through an existing administrative group. The default playbook refuses application unless explicitly authorized.

    .venv/bin/ansible-playbook playbooks/site.yml --check --diff -e '{"cis_ssh_allow_groups":["sudo"]}'
    .venv/bin/ansible-playbook playbooks/site.yml --limit staging -e '{"cis_apply_changes":true,"cis_ssh_allow_groups":["sudo"]}'

Keep console access and a second authenticated SSH session open. Firewall and PAM management are separate opt-ins. The level2 local profile adds stricter SSH session/forwarding limits; it is not a full benchmark claim.

## Start the identity lab

    python3 identity/scripts/init_env.py
    make identity-up
    # Wait for the login page at http://127.0.0.1:8080
    set -a
    source identity/docker-compose/.env
    set +a
    python3 identity/scripts/reconcile_ldap.py
    python3 identity/scripts/verify_discovery.py
    make identity-down

Realm enterprise-corp includes a public OIDC client with PKCE S256, a department scope and a placeholder SAML service provider. Replace SAML URLs and exchange metadata with your SP before authentication testing. LDAP is READ_ONLY and initially contains organizational units only; provision users through your directory administrator.

The Compose stack is loopback-only development infrastructure, with generated local secrets and persistent volumes. OpenLDAP's image requires amd64 or emulation. Production needs TLS/LDAPS, a supported directory image, restricted service credentials, external secrets, backups and a production Keycloak command. See [the runbook](docs/operations.md).

## Automation and evidence

GitHub Actions and GitLab CI validate actual configuration and tests. Weekly scheduled CI checks for regressions; it does not generate artificial code changes or audit scores. Extend the baseline only alongside coverage and an explicit control mapping.
