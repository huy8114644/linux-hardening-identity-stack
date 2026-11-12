# Identity recovery rehearsal

Use a disposable environment and an approved maintenance window. Record the Keycloak version, LDAP schema revision and database backup timestamp before starting.

1. Export the realm configuration and back up PostgreSQL and LDAP volumes through their supported backup tools. Keep secrets outside Git.
2. Restore into a separate network with a distinct issuer hostname; never point a rehearsal at production LDAP.
3. Confirm LDAP read-only federation, user lookup and group mappings; check OIDC discovery and SAML metadata against the restored issuer.
4. Sign in with a test account, verify PKCE code flow and expected client scopes, then revoke sessions and confirm access expires.
5. Record measured RTO/RPO, unresolved failures and rollback owner in an incident ticket. No recovery target is asserted until measured.

A version-controlled realm export is configuration, not a backup of passwords, keys or sessions. Protect database and LDAP backups separately.
