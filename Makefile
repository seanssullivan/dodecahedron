bdist_wheel:
	python setup.py bdist_wheel

sdist:
	python setup.py sdist

test:
	coverage run -m pytest --tb=short

tox:
	tox
