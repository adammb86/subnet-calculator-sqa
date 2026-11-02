# Subnet Calculator SQA

Aplikasi web kalkulator subnet dan VLSM berbasis FastAPI, dilengkapi pipeline SQA (Software Quality Assurance).

## Menjalankan Lokal

```bash
uv sync --dev
uv run fastapi dev main.py
```

Buka browser di `http://127.0.0.1:8000`.

## Menjalankan Test

```bash
uv run pytest test_main.py -v --cov=main --cov-report=term-missing
```

## Docker

### Build image

```bash
docker build -t subnet-calculator .
```

### Jalankan container

```bash
docker run -d --name subnet-app -p 8000:8000 subnet-calculator
```

### Smoke test container

```bash
uv run python scripts/smoke_test.py http://127.0.0.1:8000
```

### Bersihkan container

```bash
docker rm -f subnet-app
```

