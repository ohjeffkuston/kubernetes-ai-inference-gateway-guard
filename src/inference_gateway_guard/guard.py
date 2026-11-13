"""Deterministic evaluation of Kubernetes AI inference gateway contracts."""

from __future__ import annotations

from datetime import date
from typing import Any


def _check(rule: str, passed: bool, message: str, severity: str = "BLOCK") -> dict[str, Any]:
    return {"rule": rule, "passed": bool(passed), "severity": severity, "message": message}


def evaluate(document: dict[str, Any], policy: dict[str, Any], as_of: date | None = None) -> dict[str, Any]:
    """Return a stable PASS, REVIEW, or BLOCK decision with rule evidence."""
    today = as_of or date.today()
    service = document.get("service", {})
    gateway = document.get("gateway", {})
    routing = document.get("routing", {})
    protection = document.get("protection", {})
    security = document.get("security", {})
    telemetry = document.get("telemetry", {})
    reliability = document.get("reliability", {})
    validation = document.get("validation", {})
    operations = document.get("operations", {})
    rules: list[dict[str, Any]] = []

    rules.append(_check("IG-001", all(service.get(k) for k in ("name", "owner", "environment", "service_tier")), "Service identity, owner, environment, and tier are explicit"))
    rules.append(_check("IG-002", gateway.get("api_version") == "gateway.networking.k8s.io/v1" and gateway.get("inference_extension") is True and gateway.get("inference_pool") and gateway.get("inference_model"), "Stable Gateway API and inference-specific resources are declared"))
    rules.append(_check("IG-003", gateway.get("tls") is True and gateway.get("authentication") in {"oidc", "mtls"} and gateway.get("authorization") == "deny-by-default", "TLS, workload authentication, and deny-by-default authorization protect the gateway"))
    rules.append(_check("IG-004", routing.get("strategy") in {"queue-aware", "kv-cache-aware"} and routing.get("live_metrics") is True and routing.get("model_identity_required") is True, "Routing is inference-aware and driven by bounded live metrics"))
    rules.append(_check("IG-005", routing.get("criticality_classes") is True and routing.get("batch_isolated") is True and routing.get("priority_cap", 0) <= policy["max_priority_cap"], "Criticality classes cannot let batch traffic starve interactive inference"))
    rules.append(_check("IG-006", routing.get("fallback_model") and routing.get("fallback_compatible") is True and routing.get("fallback_depth") == 1, "A compatible single-hop fallback avoids retry cascades"))

    global_limit = protection.get("global_rate_limit_rpm", 0)
    local_limit = protection.get("local_burst_rps", 0)
    rules.append(_check("IG-007", 0 < global_limit <= policy["max_global_rate_limit_rpm"] and 0 < local_limit <= policy["max_local_burst_rps"], "Layered global and local limits protect shared inference capacity"))
    rules.append(_check("IG-008", 0 < protection.get("max_request_tokens", 0) <= policy["max_request_tokens"] and 0 < protection.get("max_concurrent_requests", 0) <= policy["max_concurrent_requests"], "Token and concurrency budgets bound expensive requests"))
    rules.append(_check("IG-009", 0 < protection.get("request_timeout_seconds", 0) <= policy["max_request_timeout_seconds"] and protection.get("stream_idle_timeout_seconds", 0) <= policy["max_stream_idle_timeout_seconds"], "Request and stream-idle timeouts release capacity"))
    rules.append(_check("IG-010", protection.get("circuit_breaker") is True and 0 <= protection.get("retry_budget_percent", 101) <= policy["max_retry_budget_percent"] and protection.get("retry_non_idempotent") is False, "Circuit breaking and a small retry budget prevent retry storms"))

    rules.append(_check("IG-011", security.get("prompt_payload_logging") is False and security.get("redaction") is True and security.get("secrets_from_external_store") is True, "Prompt data is not logged and secrets remain external"))
    rules.append(_check("IG-012", security.get("egress_allowlist") is True and security.get("model_endpoint_identity") is True and security.get("signed_images") is True, "Egress, backend identity, and signed images reduce supply-chain and exfiltration risk"))

    required_metrics = set(policy["required_metrics"])
    rules.append(_check("IG-013", telemetry.get("opentelemetry") is True and telemetry.get("bounded_attributes") is True and required_metrics <= set(telemetry.get("metrics", [])), "OpenTelemetry covers latency, queueing, tokens, saturation, errors, and fallback use"))
    slo = reliability.get("slo", {})
    rules.append(_check("IG-014", slo.get("availability_percent", 0) >= policy["minimum_availability_percent"] and slo.get("p95_latency_ms", 10**9) <= policy["max_p95_latency_ms"] and bool(slo.get("error_budget_policy")), "Availability, latency, and error-budget policy define reliability"))
    rules.append(_check("IG-015", reliability.get("minimum_replicas", 0) >= 2 and reliability.get("zone_spread") is True and reliability.get("pdb") is True and reliability.get("overload_shedding") is True, "Replicas, zone spread, disruption protection, and load shedding preserve service"))

    evidence = validation.get("load_test", {})
    try:
        raw = evidence.get("last_run", "1900-01-01")
        last_run = raw if isinstance(raw, date) else date.fromisoformat(str(raw))
        age = (today - last_run).days
    except (TypeError, ValueError):
        age = 10**6
    required_scenarios = {"burst", "backend_failure", "fallback", "rate_limit", "zone_loss"}
    rules.append(_check("IG-016", evidence.get("passed") is True and 0 <= age <= policy["max_evidence_age_days"] and required_scenarios <= set(evidence.get("scenarios", [])) and evidence.get("overload_rejection_accuracy_percent", 0) >= policy["minimum_overload_rejection_accuracy_percent"], "Fresh load evidence covers failure, fallback, overload, and zone loss"))

    rollout = validation.get("rollout", {})
    rules.append(_check("IG-017", rollout.get("audit_first") is True and rollout.get("canary_percent", 0) <= policy["max_canary_percent"] and rollout.get("automatic_rollback") is True and rollout.get("human_approval") is True, "Gateway policy changes use audit-first canaries, rollback, and approval"))

    operational = all(operations.get(k) for k in ("runbook", "dashboard", "alert_route", "review_owner"))
    rules.append(_check("IG-018", operational, "Runbook, dashboard, alert route, and review owner are recorded", "REVIEW"))

    failed = [rule for rule in rules if not rule["passed"]]
    decision = "BLOCK" if any(rule["severity"] == "BLOCK" for rule in failed) else "REVIEW" if failed else "PASS"
    score = round(100 * (len(rules) - len(failed)) / len(rules), 1)
    return {"decision": decision, "score": score, "passed": len(rules) - len(failed), "total": len(rules), "rules": rules}
