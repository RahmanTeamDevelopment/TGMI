PY=tgmi/*.py
PEP8=pep8 --max-line-length=120

env:
	virtualenv -p python2.7 env
	pip install -U pip
	pip install -r requirements.txt --no-cache-dir --ignore-installed

clean:
	pip uninstall -y TGMI
	find . -name __pycache__ | xargs rm -rf

cleanAll: clean
	rm -rf env

pep8:
	${PEP8} ${PY}

install: env
	pip install -U .

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
