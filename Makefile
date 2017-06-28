PY=tgmi/*.py
PEP8=pep8 --max-line-length=120

clean:
	pip uninstall -y TGMI
	find . -name __pycache__ | xargs rm -rf

cleanAll: clean
	rm -rf env

pep8:
	${PEP8} ${PY}

install:
	./install.sh

wheels:
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
