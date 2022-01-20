init:
	pip install -r requirements.txt

setup: requirements.txt
	pip install -r requirements.txt

run:
	python core.py

clean:
    rm -rf __pycache__