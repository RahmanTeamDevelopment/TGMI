PY=tgmi/*.py
PEP8=pep8 --max-line-length=120
FLAKE8=flake8 --max-line-length=120
PYLINT=pylint --max-line-length=120 -d C0111

clean:
	pip uninstall -y TGMI
	find . -name __pycache__ | xargs rm -rf

cleanAll: clean
	rm -rf env

pep8:
	${PEP8} ${PY}

flake8:
	${FLAKE8} ${PY}

pylint:
	${PYLINT} ${PY}

install:
	./install.sh

wheels:
	pip wheel .

unittest: install
	@echo ''
	@echo 'Running unit tests'
	@echo ''
	@pytest test/unit

test: pep8 flake8 unittest
	@echo ''
	@echo 'Finished running all tests'
	@echo ''

test_coverage:
	py.test --cov-report term-missing --cov=env/lib/python2.7/site-packages/tgmi/ test/
