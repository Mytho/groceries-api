all: help

help:
	@echo 'check   -- check the code syntax'
	@echo 'clean   -- cleanup the environment'
	@echo 'help    -- display this information'
	@echo 'httpd   -- start a local development server'
	@echo 'user    -- add a user account'
	@echo 'test    -- run the unittests'

check:
	flake8 --show-source bin application tests

clean:
	find . -name '__pycache__' -delete -o -name '*.pyc' -delete

httpd:
	./bin/httpd.py -H 0.0.0.0 -p 8002 -d

user:
	./bin/add-user.py

test:
	coverage run --source application,clock --module pytest tests --assert=plain
	coverage report --fail-under=100 --show-missing
