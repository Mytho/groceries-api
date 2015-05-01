all: help

help:
	@echo 'check     -- check the code syntax'
	@echo 'clean     -- cleanup the environment'
	@echo 'help      -- display this information'
	@echo 'httpd     -- start a local development server'
	@echo 'install   -- install all dependencies'
	@echo 'test      -- test the all code'
	@echo 'unittest  -- run the unittests'
	@echo 'uninstall -- uninstall all dependencies'

clean:
	find . -name '__pycache__' -delete -o -name '*.pyc' -delete

httpd:
	./bin/httpd.py -H 0.0.0.0 -p 8002 -d

user:
	./bin/add-user.py

# Installation of dependencies

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

uninstall:
	- pip freeze | xargs pip uninstall --yes

# Automated testing

check:
	flake8 bin
	flake8 application
	flake8 tests

unittest:
	coverage run --source application --module pytest tests
	coverage report --fail-under=100 --show-missing

test: uninstall clean install check unittest

# DB Migrations

migrate:
	alembic upgrade head

upgrade:
	alembic upgrade +1

downgrade:
	alembic downgrade -1
