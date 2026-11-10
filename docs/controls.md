# Control coverage and scope

| Area | Implemented | Verification / remaining work |
|---|---|---|
| SSH | non-root, keys only, restricted groups, idle limits, optional forwarding limits | template tests + Molecule; verify effective sshd configuration and access on VMs |
| PAM | pwquality; RHEL authselect with faillock | opt-in; Ubuntu lockout is not configured |
| Audit | identity, sudoers, SSH watches | file deployment; privileged kernel audit behavior needs VM testing |
| Firewall | UFW on Debian, dedicated nftables table on RHEL | opt-in; rule syntax validates before installation; connectivity needs VM test |
| Filesystems | selected module denylist | existing loaded modules and mounted filesystems are untouched |
| Kernel | redirect rejection, ASLR, syncookies, core-dump restrictions | host-only; activation needs VM verification |
| Identity | realm, PKCE OIDC, department claim scope, SAML SP template, read-only LDAP component | offline contracts; discovery verifier checks endpoints, not a complete login |

Target environments: Ubuntu 22.04 and RHEL 9 compatible hosts. Only Ubuntu is configured in the initial Molecule scenario. RHEL configuration remains unverified on a real RHEL VM. Changes to PAM must account for SSSD/AD authentication requirements. Do not apply these networking defaults to routers or Kubernetes nodes without a separate profile.

Full CIS profiles also require partitions, mount flags, time synchronization, bootloader controls, package/service review, account lifecycle and more. Use benchmark guidance and an independent assessment for compliance claims.
