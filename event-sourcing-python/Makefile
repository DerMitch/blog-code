.PHONY: all init

all:
	@echo "Please specify a target"

init:
	rm -rf ./venv
	python3 -m venv ./venv
	./venv/bin/pip install -U pip wheel
	./venv/bin/pip install -U -r requirements.txt

lint:
	@echo "=============== Running mypy (Type Checks) ==============="
	./venv/bin/mypy state_manager.py
	@echo

	@echo "=============== Running pylint (Code Checks) ==============="
	./venv/bin/pylint state_manager.py
	@echo

test:
	@echo "=============== Running pytest (Unit Tests) ==============="
	./venv/bin/pytest --cov-report term-missing --cov=state_manager
