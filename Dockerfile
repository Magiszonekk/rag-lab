# RAG Lab API — obraz dla Kubernetesa (chart deploy/helm/raglab) i Docker Compose.
# Korpus nie jest w obrazie: buduje go Job ingestu (PDF z API Sejmu → JSON) na wolumenie danych.
# Na serwerze domowym API działa z systemd (uv), ten obraz służy klastrowi (kind w CI, AKS w M4).

FROM python:3.12-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.11.7 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app
# najpierw same zależności (warstwa cache), potem kod
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-install-project
COPY src ./src
COPY README.md LICENSE ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev
# zapasowy model wektorów (mmlw, ~0,5 GB) w obrazie: pod nie pobiera go z Hugging Face przy starcie
ARG WITH_MMLW=1
RUN if [ "$WITH_MMLW" = "1" ]; then \
      HF_HOME=/app/hf /app/.venv/bin/python -c \
      "from sentence_transformers import SentenceTransformer as S; S('sdadas/mmlw-roberta-base', device='cpu')"; \
    else mkdir -p /app/hf; fi

FROM python:3.12-slim
RUN useradd --uid 10001 --create-home raglab
WORKDIR /app
COPY --from=build --chown=10001:10001 /app/.venv /app/.venv
COPY --from=build --chown=10001:10001 /app/hf /app/hf
COPY --chown=10001:10001 src ./src
COPY --chown=10001:10001 deploy/helm/raglab/files/db-init ./db/init
COPY --chown=10001:10001 data/sources.toml ./data/sources.toml
COPY --chown=10001:10001 data/annotations ./data/annotations
COPY --chown=10001:10001 data/eval ./data/eval
COPY --chown=10001:10001 results ./results
COPY --chown=10001:10001 web/public/examples.json ./web/public/examples.json
# korpus i cache na wolumenie (data/corpus, data/raw, data/cache są dowiązane do /data)
RUN mkdir -p /data/corpus /data/raw /data/cache && chown -R 10001:10001 /data \
    && ln -s /data/corpus data/corpus && ln -s /data/raw data/raw && ln -s /data/cache data/cache
ENV PATH=/app/.venv/bin:$PATH PYTHONUNBUFFERED=1 HF_HOME=/app/hf HF_HUB_OFFLINE=1 \
    RAGLAB_LAW_WATCH=/data/law_watch.json
USER 10001
EXPOSE 8000
CMD ["uvicorn", "raglab.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--proxy-headers"]
