To: ohjeffkuston@yahoo.ca
Subject: Day 30 — Kubernetes AI Inference Gateway Guard

# Deployment, learning, and interview positioning

The Day 30 project is a deterministic GitOps policy gate for production Kubernetes AI inference gateways. It addresses a current platform problem: ordinary load balancing cannot see model identity, queue depth, KV-cache locality, request criticality, token cost, or accelerator saturation.

## What was implemented

- 18 deterministic controls with PASS, REVIEW, and BLOCK decisions
- Stable Gateway API and inference-extension evidence
- Queue-aware routing, bounded criticality, and one-hop compatible fallback
- Layered global/local limits, token and concurrency budgets, timeouts, circuit breaker, and retry budget
- Prompt privacy, redaction, external secrets, egress controls, backend identity, and signed images
- OpenTelemetry metrics, SLOs, overload shedding, fresh load evidence, canary, rollback, and approval
- CLI, compliant/unsafe samples, 20 tests, GitHub Actions, non-root Docker image, architecture visual, research, and deployment guidance

## Safe deployment

Use audit mode first, reconcile contract claims to live gateway state, and run burst/failure/fallback tests only in isolated non-production environments with cost and duration limits. Canary enforcement on at most 10% of traffic. Roll back automatically on SLO regression and require human approval for promotion. The repository never mutates a cluster.

## Learning

Inference routing is a scheduling problem as much as a networking problem. Global and local rate limits protect different failure modes. Retries and fallbacks can amplify an outage. Bounded telemetry and representative load evidence are necessary because a valid manifest does not prove safe runtime behaviour.

## Interview positioning

Use the project to explain the production problem, why inference differs from stateless HTTP, the choice of deterministic enforcement, layered overload controls, privacy boundaries, measurable outcomes, failure-mode analysis, and audit-first rollout. It demonstrates practical Kubernetes, SRE, DevOps, platform engineering, security, and AI-infrastructure judgment.

Repository: https://github.com/ohjeffkuston/kubernetes-ai-inference-gateway-guard
