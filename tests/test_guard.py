from copy import deepcopy
from datetime import date
from pathlib import Path

import pytest
import yaml

from inference_gateway_guard import evaluate

ROOT = Path(__file__).parents[1]
POLICY = yaml.safe_load((ROOT / "policy/gateway-policy.yaml").read_text())
GOOD = yaml.safe_load((ROOT / "samples/compliant-gateway.yaml").read_text())
BAD = yaml.safe_load((ROOT / "samples/unsafe-gateway.yaml").read_text())
AS_OF = date(2026, 11, 13)


def test_compliant_gateway_passes_all_controls():
    result = evaluate(GOOD, POLICY, AS_OF)
    assert result["decision"] == "PASS"
    assert result["score"] == 100.0
    assert result["passed"] == result["total"] == 18


def test_unsafe_gateway_blocks():
    result = evaluate(BAD, POLICY, AS_OF)
    assert result["decision"] == "BLOCK"
    assert result["score"] < 10


@pytest.mark.parametrize(
    ("mutate", "rule"),
    [
        (lambda d: d["service"].pop("owner"), "IG-001"),
        (lambda d: d["gateway"].update(inference_extension=False), "IG-002"),
        (lambda d: d["gateway"].update(tls=False), "IG-003"),
        (lambda d: d["routing"].update(strategy="round-robin"), "IG-004"),
        (lambda d: d["routing"].update(batch_isolated=False), "IG-005"),
        (lambda d: d["routing"].update(fallback_depth=3), "IG-006"),
        (lambda d: d["protection"].update(global_rate_limit_rpm=0), "IG-007"),
        (lambda d: d["protection"].update(max_request_tokens=99999), "IG-008"),
        (lambda d: d["protection"].update(request_timeout_seconds=999), "IG-009"),
        (lambda d: d["protection"].update(retry_budget_percent=50), "IG-010"),
        (lambda d: d["security"].update(prompt_payload_logging=True), "IG-011"),
        (lambda d: d["security"].update(signed_images=False), "IG-012"),
        (lambda d: d["telemetry"].update(bounded_attributes=False), "IG-013"),
        (lambda d: d["reliability"]["slo"].update(p95_latency_ms=5000), "IG-014"),
        (lambda d: d["reliability"].update(overload_shedding=False), "IG-015"),
        (lambda d: d["validation"]["load_test"].update(last_run="2025-01-01"), "IG-016"),
        (lambda d: d["validation"]["rollout"].update(human_approval=False), "IG-017"),
    ],
)
def test_control_regressions_block(mutate, rule):
    candidate = deepcopy(GOOD)
    mutate(candidate)
    result = evaluate(candidate, POLICY, AS_OF)
    assert result["decision"] == "BLOCK"
    assert rule in {item["rule"] for item in result["rules"] if not item["passed"]}


def test_missing_operational_evidence_requires_review():
    candidate = deepcopy(GOOD)
    candidate["operations"].pop("runbook")
    result = evaluate(candidate, POLICY, AS_OF)
    assert result["decision"] == "REVIEW"
    assert result["score"] == 94.4
