
.PHONY: all init

all:
	@echo "Please specify a target"

init:
	python3 -m venv ./venv
	./venv/bin/pip install -U pip wheel
	./venv/bin/pip install -U -r requirements.txt

server:
	FLASK_APP=server:app FLASK_ENV=development ./venv/bin/flask run
