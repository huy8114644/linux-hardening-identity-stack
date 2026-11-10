# Operating procedures

## Staging and rollback

1. Snapshot the VM, export firewall rules and copy SSH, PAM, security, audit, sysctl and modprobe configurations.
2. Confirm console recovery and an existing key-based administrator account. Review check-mode diff.
3. Apply to one staging host. Verify a new SSH connection before ending the existing session.
4. Check effective SSH settings, loaded audit rules, sysctl output and firewall connectivity. Reboot and verify persistence.
5. Restore saved configurations and reload affected services to roll back. Use the VM snapshot for authentication lockout recovery.

The role never unloads filesystem modules or flushes unrelated firewall tables. The SSH port and firewall allow list must agree. nftables enables a default-deny input chain; review compatibility with firewalld before opting in.

## Identity lifecycle

The environment generator creates a mode-0600 .env and refuses to overwrite it. Keycloak realm import occurs on initial startup; it does not reconcile an existing realm. The LDAP reconciler creates or updates one named component and never logs credentials.

The included bind account is the lab LDAP administrator. Production requires a read-only service DN with explicit directory ACLs. There are no sample user passwords or test employees. Establish an LDAP user, perform an OIDC authorization-code + PKCE login and test a SAML SP separately before claiming federation works end to end.

Stopping Compose keeps volumes. Back up PostgreSQL with pg_dump and LDAP with slapcat; test restoration. Credential rotation must coordinate persisted service state; changing .env alone does not rotate existing credentials.

Do not expose start-dev or plaintext LDAP outside the isolated local lab. Configure TLS, hostname validation, production Keycloak settings, external secrets, least-privilege LDAP bind, network isolation, monitoring and disaster recovery for deployment.
