SHELL := /bin/bash
VENV ?= .venv
BIN := $(abspath $(VENV))/bin
export PATH := $(BIN):$(PATH)
.PHONY: setup check molecule identity-up identity-down
setup:
	python3 -m venv $(VENV)
	$(BIN)/pip install -r requirements-dev.txt
	$(BIN)/ansible-galaxy collection install -r requirements.yml

check:
	$(BIN)/ruff check identity/scripts tests
	$(BIN)/pytest -q
	$(BIN)/ansible-playbook --syntax-check playbooks/site.yml
	DB_PASSWORD=validation LDAP_ADMIN_PASSWORD=validation KEYCLOAK_ADMIN_PASSWORD=validation docker compose -f identity/docker-compose/docker-compose.yml config --quiet

molecule:
	cd roles/cis_hardening && ANSIBLE_ROLES_PATH=$(CURDIR)/roles $(BIN)/molecule test

identity-up:
	cd identity/docker-compose && docker compose up -d

identity-down:
	cd identity/docker-compose && docker compose down
