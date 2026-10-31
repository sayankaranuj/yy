.PHONY: test test-unit test-integration test-api test-security test-pipeline test-performance test-frontend test-all coverage docker-test lint format

test:
	pytest tests/ -m "not live and not e2e" -q

test-unit:
	pytest tests/ -m unit -q

test-integration:
	pytest tests/ -m integration -q

test-api:
	pytest tests/ -m api -q

test-security:
	pytest tests/ -m security -q

test-pipeline:
	pytest tests/ -m agent -q

test-performance:
	pytest tests/ -m slow -q

test-frontend:
	cd frontend && npm run test

test-all:
	pytest tests/ -m "not live and not e2e and not slow" -q
	cd frontend && npm run test

coverage:
	pytest tests/ -m "not live and not e2e and not slow" --cov=backend --cov-report=term-missing --cov-report=html:coverage_report

docker-test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
	docker compose -f docker-compose.test.yml down

lint:
	ruff check backend/ tests/

format:
	black backend/ tests/