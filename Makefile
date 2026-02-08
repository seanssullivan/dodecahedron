build:
	hatch build

test:
	coverage run -m pytest --tb=short

tox:
	tox
