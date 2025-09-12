COVERAGE = --cov=. --cov-report=term-missing

.PHONY: all
all: test

.PHONY: test
test:
	uv run pytest

.PHONY: cov
cov:
	uv run pytest $(COVERAGE)

.PHONY: lint
lint:
	uv tool run ruff check .
	uv tool run ty check .
