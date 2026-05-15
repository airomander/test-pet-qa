FROM python:3.12-slim

RUN pip install poetry==2.4.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction

COPY . .

RUN playwright install chromium

CMD ["pytest", "tests/", "-v", "--alluredir=allure-results"]
