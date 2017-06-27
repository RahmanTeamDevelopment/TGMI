PY=tgmi/*.py
PEP8=pep8 --max-line-length=120

pep8:
	${PEP8} ${PY}

wheels: env
	pip wheel .

unittest: install
	@echo ''
	@echo 'Running unit tests'
	@echo ''
	@pytest test/unit

test: pep8 unittest
	@echo ''
	@echo 'Finished running all tests'
	@echo ''

test_coverage:
	pytest --cov=coverview test
