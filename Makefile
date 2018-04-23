test:
	python3 -m unittest discover
	python2 -m unittest discover

uppload:
	mkdir -p dist.old
	mv dist/* dist.old/
	python setup.py sdist
	twine upload dist/*
