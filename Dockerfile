# =========================
# Dev / Build Stage
# =========================
FROM python:3.11-slim AS dev

WORKDIR /radar

# System dependencies (build + postgres + pcre)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    git \
    curl \
    libpq-dev \
    libpcre2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.3
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

# Poetry settings
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

# Copy dependency files first (better caching)
COPY pyproject.toml poetry.lock* /radar/

# Install dependencies
RUN poetry install --with dev

# Copy source
COPY . /radar

# Install project itself
RUN poetry install --with dev

# Environment variables (DEV)
ENV RADAR_SETTINGS=/radar/example_settings.py \
    FLASK_ENV=development \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8


# =========================
# Production Stage
# =========================
FROM python:3.11-slim AS prod

WORKDIR /srv/radar

# Runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    libpcre2-8-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages + app
COPY --from=dev /usr/local /usr/local
COPY --from=dev /radar /srv/radar

# IMPORTANT: match production path
ENV RADAR_SETTINGS=/srv/radar/example_settings.py \
    FLASK_ENV=production \
    PYTHONUNBUFFERED=1 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Create non-root user
RUN useradd -ms /bin/bash radar
USER radar

EXPOSE 5000

# Adjust if your real entrypoint differs
CMD ["python", "-m", "radar"]
