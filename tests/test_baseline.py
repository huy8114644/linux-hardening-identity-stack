import importlib.util
import json
from pathlib import Path

import pytest
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[1]


def test_all_yaml_documents_parse():
    paths = list(ROOT.glob("roles/**/*.yml")) + list(ROOT.glob("playbooks/*.yml"))
    paths += [ROOT / ".gitlab-ci.yml", ROOT / "identity/docker-compose/docker-compose.yml"]
    assert paths
    for path in paths:
        assert yaml.safe_load(path.read_text()) is not None, path


def test_ssh_template_renders_both_profiles_and_custom_port():
    role = ROOT / "roles/cis_hardening"
    defaults = yaml.safe_load((role / "defaults/main.yml").read_text())
    template = Environment(loader=FileSystemLoader(role / "templates")).get_template(
        "ssh-hardening.conf.j2"
    )
    for level in ("level1", "level2"):
        settings = defaults | {
            "cis_profile": level, "cis_ssh_port": 2222, "cis_ssh_allow_groups": ["ops"],
        }
        rendered = template.render(**settings)
        assert "Port 2222" in rendered
        assert "AllowGroups ops" in rendered
        assert "PermitRootLogin no" in rendered
        assert ("AllowAgentForwarding no" in rendered) == (level == "level2")


def test_defaults_require_opt_in():
    defaults = yaml.safe_load((ROOT / "roles/cis_hardening/defaults/main.yml").read_text())
    assert defaults["cis_apply_changes"] is False
    assert defaults["cis_manage_firewall"] is False
    assert defaults["cis_manage_pam"] is False


def test_realm_uses_pkce_without_implicit_or_password_grants():
    realm = json.loads((ROOT / "identity/keycloak/realms/enterprise-corp-realm.json").read_text())
    client = next(c for c in realm["clients"] if c["protocol"] == "openid-connect")
    assert client["attributes"]["pkce.code.challenge.method"] == "S256"
    assert not client["directAccessGrantsEnabled"]
    assert not client["implicitFlowEnabled"]
    assert realm["registrationAllowed"] is False


def test_federation_is_read_only_and_scoped():
    spec = importlib.util.spec_from_file_location(
        "reconcile", ROOT / "identity/scripts/reconcile_ldap.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    config = module.federation("realm-id", "test-password")
    assert config["parentId"] == "realm-id"
    assert config["config"]["editMode"] == ["READ_ONLY"]
    assert config["config"]["usersDn"] == ["ou=people,dc=enterprise,dc=internal"]
    with pytest.raises(ValueError, match="loopback"):
        module.reconcile("http://example.invalid", "test", "test")
