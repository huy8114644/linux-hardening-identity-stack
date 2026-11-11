# Contributing

Start with [AGENTS.md](AGENTS.md) and follow the README's local quickstart. Keep changes small, explain their operational purpose, and update documentation when configuration or behavior changes. Use conventional commits, for example `docs: clarify local validation` or `fix: handle a missing field`.

Before requesting review, run the applicable Makefile checks and attach concise, sanitized command output with tool versions. Distinguish checks that passed, failed, or were not run; state the reason for each limitation. A workflow definition is not proof that the workflow passed. Do not report synthetic data as operational evidence.

Run `make lint`, `make test`, `make plan`, and `make scan`. A missing scanner or a scan finding is a failed gate. Scan covers current working-tree files rather than Git history. Never commit credentials, tokens, generated secrets, real inventory reports or environment directories.

Use the pull request template. Identify configuration changes, compatibility risks, validation evidence and a recovery procedure. Ask reviewers to inspect the diff and test results before merging; this is a review convention, not a claim that branch protection is configured.

Linux-specific validation: run `make check` for offline contracts, Ansible syntax and Compose configuration. For role changes, run `make molecule` only on a dedicated disposable Docker daemon. Host control changes need staging VM evidence and recovery planning; a container cannot verify kernel enforcement or full CIS compliance. Do not run a host apply as part of ordinary development. Identity bootstrap and full OIDC/SAML login validation are separate explicit lab actions; report their actual scope.
