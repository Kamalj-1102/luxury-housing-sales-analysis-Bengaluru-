install:
	pip install -r requirements.txt

sample:
	python scripts/generate_sample_data.py

etl:
	python -m src.pipeline --input data/raw/sample_luxury_housing_sales.csv

test:
	pytest -q
