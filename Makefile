test:
	python3 -m unittest discover
	python2 -m unittest discover

uppload:
	python setup.py sdist
	twine upload dist/*
