clean: install
	rm -rf build dist .eggs *.egg-info

requirements:
	echo Installing requirements ...
	pip install -r requirements.txt

install: requirements
	python setup.py install