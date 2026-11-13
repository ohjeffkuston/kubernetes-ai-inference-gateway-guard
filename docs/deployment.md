# Safe deployment guide

1. Export proposed Gateway API, InferencePool, InferenceModel, traffic policy, SLO, and load-test evidence into a contract matching `samples/compliant-gateway.yaml`.
2. Run the guard in CI and begin with `REVIEW` results as non-blocking annotations.
3. Compare contract evidence with live gateway configuration and telemetry; do not treat self-reported YAML as runtime proof.
4. Exercise burst, backend failure, fallback, global/local rate limiting, and zone loss only in an isolated non-production environment with cost and duration ceilings.
5. Canary enforcement on at most 10% of traffic, monitor latency, errors, fallbacks, rejected overload, token use, and saturation, then require a human approval before promotion.
6. Roll back the policy commit automatically if error-budget burn or p95 latency exceeds the declared threshold.

The repository never changes a cluster. Production admission, Envoy/Gateway API reconciliation, Redis-backed global limits, secrets, and telemetry backends remain explicit operator-owned extensions.

## Security and privacy

- Do not put prompts, responses, credentials, access tokens, or customer data in contracts or CI artifacts.
- Disable prompt-payload logging; prefer redacted metadata and bounded OpenTelemetry attributes.
- Authenticate clients and model backends, default-deny authorization, allowlist egress, and verify signed images.
- Treat fallbacks as a data-governance boundary: compatibility includes policy, privacy, region, and model capability—not only API shape.

## Failure modes

- Local limits multiply with proxy replicas and reset on restart; use a global service for shared quotas.
- Retries can amplify overload and duplicate non-idempotent inference work.
- An unhealthy fallback can create a second failure domain.
- Stale queue or KV-cache metrics can make inference-aware routing worse than simple balancing.
- Strict timeouts can terminate valid long-running streams; validate them with representative traffic.
