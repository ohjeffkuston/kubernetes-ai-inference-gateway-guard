# Demand validation

Checked 2026-11-13 (America/Detroit).

## Authoritative technical sources

- [Kubernetes: Introducing Gateway API Inference Extension](https://kubernetes.io/blog/2025/06/05/introducing-gateway-api-inference-extension/) documents inference-aware endpoint selection using queue length, memory, loaded adapters, request criticality, and model identity rather than ordinary round-robin routing.
- [Envoy Gateway rate-limiting concepts](https://gateway.envoyproxy.io/docs/concepts/rate-limiting/) distinguishes coordinated global limits from fast local limits and recommends both for fair usage and overload protection.
- [Envoy Gateway global rate-limit task](https://gateway.envoyproxy.io/docs/tasks/traffic/global-rate-limit/) shows platform-level and route-level policy merging for shared limits.
- [Envoy Gateway connection limits](https://gateway.envoyproxy.io/docs/tasks/traffic/connection-limit/) explains why gateways need explicit concurrency protection.

## Live demand evidence

- [Nexera — AI Infrastructure & LLM Inference Engineer](https://jobs.gusto.com/postings/nexera-ai-infrastructure-llm-inference-engineer-97163c7d-5f1c-4927-8a55-8fe0f9cbdb34) lists Kubernetes/OpenShift, vLLM/Triton/Ray Serve, NGINX or LiteLLM gateways, OIDC/JWT, TLS, and production troubleshooting; listed base salary is $175,000–$225,000.
- [WorkOS — Infrastructure Engineer, SRE](https://jobs.ashbyhq.com/workos/cff5a16f-fd1c-4b64-9b66-8a8321122375) emphasizes resilient infrastructure, observability, incident response, and AI-company workloads; listed US base salary is $175,000–$275,000.
- [Modular — Cloud Inference Engineer](https://www.builtinsf.com/job/cloud-inference-engineer/11927887) calls for Kubernetes operators, Helm, high-scale LLM inference, networking, distributed caching, and platform performance; listed US base salary is $180,000–$270,000.

## Why this project

The recurring requirement is not a generic chatbot. Teams need engineers who can operate model-serving gateways under overload, secure tenant traffic, reason about GPU-backed routing, and prove reliability with telemetry and load evidence. This project converts those demands into a deterministic, testable GitOps gate.
