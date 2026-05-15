# QA Automation Pet-Project

Automated test framework for [SauceDemo](https://www.saucedemo.com) + [ReqRes](https://reqres.in) API.

**Stack:** Python, Playwright, pytest, Allure, Docker, GitHub Actions

---

## Quick start

```bash
# Install dependencies
poetry install

# Install Playwright browser
poetry run playwright install chromium

# Run all tests
poetry run pytest
```

## Test structure

```
features/           BDD scenarios (pytest-bdd)
pages/              Page Objects (UI)
api_clients/        API client (ReqRes)
schemas/            Pydantic validation models
tests/
├── ui/             UI tests (Playwright + Page Object)
├── api/            API tests (requests + Pydantic)
├── data/           Data-driven tests (JSON, CSV)
└── visual/         Visual regression (screenshots)
```

## CI / CD

```yaml
ui-tests:    3 parallel shards → Allure results
api-tests:   full API suite
allure-report: → GitHub Pages
```

## Docker

```bash
docker-compose up
```

## Allure report

```bash
poetry run pytest --alluredir=allure-results
allure generate allure-results --clean -o allure-report
allure open allure-report
```

---

[![CI](https://github.com/airomander/test-pet-qa/actions/workflows/ci.yml/badge.svg)](https://github.com/airomander/test-pet-qa/actions/workflows/ci.yml)
