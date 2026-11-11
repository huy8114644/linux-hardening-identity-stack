SHELL := /bin/bash
.DEFAULT_GOAL := help
VENV ?= .venv
BIN := $(abspath $(VENV))/bin
GITLEAKS_IMAGE ?= zricethezav/gitleaks:v8.24.3
export PATH := $(BIN):$(PATH)
.PHONY: help setup check test lint scan plan molecule identity-up identity-down

help:
	@echo "Targets: setup lint test scan plan check molecule identity-up identity-down"
	@echo "setup: install local dependencies; lint/test/plan: offline checks"
	@echo "scan: Gitleaks working tree scan (CLI or Docker; fails closed)"
	@echo "check: lint + test + plan; molecule: privileged disposable Docker integration"
	@echo "identity-up/down: explicitly start/stop local lab; down retains volumes"

setup:
	python3 -m venv $(VENV)
	$(BIN)/pip install -r requirements-dev.txt
	$(BIN)/ansible-galaxy collection install -r requirements.yml

lint:
	$(BIN)/ruff check identity/scripts tests

test:
	$(BIN)/pytest -q

plan:
	$(BIN)/ansible-playbook --syntax-check playbooks/site.yml
	DB_PASSWORD=validation LDAP_ADMIN_PASSWORD=validation KEYCLOAK_ADMIN_PASSWORD=validation docker compose -f identity/docker-compose/docker-compose.yml config --quiet

check: lint test plan

scan:
	@if command -v gitleaks >/dev/null 2>&1; then \
		gitleaks detect --no-git --source . --redact; \
	elif command -v docker >/dev/null 2>&1; then \
		docker run --rm -v "$(CURDIR):/repo:ro" $(GITLEAKS_IMAGE) detect --no-git --source /repo --redact; \
	else \
		echo "Install Gitleaks or Docker to run the required scan." >&2; exit 1; \
	fi

molecule:
	cd roles/cis_hardening && ANSIBLE_ROLES_PATH=$(CURDIR)/roles $(BIN)/molecule test

identity-up:
	cd identity/docker-compose && docker compose up -d

identity-down:
	cd identity/docker-compose && docker compose down
