FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    default-jdk-headless \
    bash \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir fastapi uvicorn

COPY . /app/

RUN chmod +x /app/demo_repo/run_all_coba_demos.sh \
    /app/demo_repo/ci/oneci_headless_gate.sh \
    /app/demo_repo/verify_5_tiers.py

ENV PORT=8080
EXPOSE 8080

CMD ["python3", "/app/app.py"]
