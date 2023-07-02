.DEFAULT_GOAL := run

dependencies:
	pipenv sync

prepare: dependencies
	pipenv run python src/1_prepare_data.py

run: dependencies prepare
	pipenv run python src/2_creating_map.py

convert: 
	jupyter nbconvert --to python src/*.ipynb 