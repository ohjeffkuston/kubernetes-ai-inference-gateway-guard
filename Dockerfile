FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY policy ./policy
COPY samples ./samples
USER 65532:65532
ENTRYPOINT ["inference-gateway-guard"]
