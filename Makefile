test:
	pytest -m "not integration" tests/

test-integration:
	pytest -m "integration" tests/
