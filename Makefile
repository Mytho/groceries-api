all: help

help:
	@echo 'check     -- check the code syntax'
	@echo 'clean     -- cleanup the environment'
	@echo 'help      -- display this information'
	@echo 'httpd     -- start a local development server'
	@echo 'install   -- install all dependencies'
	@echo 'user      -- add a user account'
	@echo 'unittest  -- run the unittests'

check:
	flake8 --show-source bin application tests

clean:
	find . -name '__pycache__' -delete -o -name '*.pyc' -delete

httpd:
	./bin/httpd.py -H 0.0.0.0 -p 8002 -d

user:
	./bin/add-user.py

unittest:
	coverage run --source application --module pytest tests --assert=plain
	coverage report --fail-under=100 --show-missing
