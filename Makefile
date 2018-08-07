init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run pylint actionqueues
	pipenv run pytest --cov-config .coveragerc  --cov=actionqueues actionqueues
	coverage report -m --fail-under 95
