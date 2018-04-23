.PHONY: test test2 test3
test2:
	python2 -m unittest discover

test3:
	python3 -m unittest discover || true

test: test3 test2

uppload:
	mkdir -p dist.old
	mv dist/* dist.old/
	python setup.py sdist
	twine upload dist/*
