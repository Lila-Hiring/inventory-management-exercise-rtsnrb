.PHONY: lint-fix help install dev lint type-check test clean build-client login coverage

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

lint-fix:  ## Fix style issues with ruff
	uv run ruff format .
	uv run ruff check --fix .

login:  ## Login to AWS CodeArtifact
	aws codeartifact get-authorization-token \
		--domain lila-prod \
		--domain-owner 579102688835 \
		--query authorizationToken \
		--output text

install:  ## Install production dependencies
	uv sync --all-extras
	uv run pre-commit install

lint:  ## Run ruff linter
	uv run ruff check .
	uv run ruff format --check .

type-check:  ## Run pyright type checker
	uv run pyright src

test:  ## Run tests with pytest
	uv run pytest src/inventory_management_exercise -v --cov=src --cov-report=term-missing:skip-covered --cov-report=xml

BASE_BRANCH ?= origin/main
coverage:  ## Display test coverage report
	uv run coverage report --format=text --show-missing --skip-covered
	uv run diff-cover coverage.xml --compare-branch=$(BASE_BRANCH)

dev:  ## Run development server
	uv run uvicorn inventory_management_exercise.main:app --reload --port 8080

clean:  ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

build-client:  ## Generate OpenAPI client
	mkdir -p clients/typescript
	openapi-generator-cli generate \
		-i http://localhost:8080/openapi.json \
		-g typescript-fetch \
		-o clients/typescript \
		--additional-properties=supportsES6=true,npmName=inventory_management_exercise-client
