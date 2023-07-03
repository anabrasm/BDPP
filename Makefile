.DEFAULT_GOAL := run

dependencies:
	pipenv sync

clean: dependencies
	pipenv run python src/clean_data.py

process: dependencies clean
	pipenv run python src/process_data.py

run: dependencies process 
	pipenv run python src/run_app.py
