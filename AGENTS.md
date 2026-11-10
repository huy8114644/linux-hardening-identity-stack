# Repository Guidelines

## Project Structure & Module Organization

The Ansible role lives in roles/cis_hardening/, including defaults, OS mappings, tasks, handlers and templates. The site playbook targets the inventory's linux_hardened group. The identity directory holds Compose services, realm JSON, LDAP bootstrap and Python administration scripts. Offline checks live in tests/, and docs/ describes scope and operations.

## Build, Test, and Development Commands

Run make setup to create .venv and install Python dependencies and Ansible collections. Run make check for Ruff, Pytest, Ansible syntax and Compose validation without applying host changes. Run make molecule to test convergence, idempotence and configuration in a disposable privileged Docker target. Use a dedicated test daemon.

Generate local credentials with python3 identity/scripts/init_env.py before make identity-up. Stop services with make identity-down; volumes persist.

## Coding Style & Naming Conventions

Use two spaces in YAML, four spaces in Python, descriptive task names and fully qualified Ansible module names. Role variables use the cis_ prefix. Python functions and files use snake_case. Ruff checks imports and correctness. Keep templates small and platform-specific behavior explicit.

## Testing Guidelines

Name Pytest files tests/test_*.py. Cover meaningful failure cases and defaults when adding controls or bootstrap logic. Update Molecule verification for deployed configuration changes. Never use production hosts for integration tests. Container tests cannot establish kernel enforcement or full CIS compliance; document VM validation separately.

## Commit & Pull Request Guidelines

Use conventional commits such as feat(identity): add LDAP group mapper. PR descriptions must identify the behavior changed, validation performed and relevant lockout or compatibility risk. Include control scope and a recovery procedure for authentication/firewall changes.

## Security & Configuration

Keep generated .env, credentials and user exports out of Git. Preserve explicit application opt-ins. Do not fabricate compliance results, work history or successful authentication evidence. Require actual test output before reporting a control as verified.
