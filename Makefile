SHELL:=/bin/bash

# ---------------------------------------------------------------------------------------------------------------------
# Environment setup and management
# ---------------------------------------------------------------------------------------------------------------------
setup-env:
	python3 -m venv ./venv && source venv/bin/activate
	python3 -m pip install -r requirements.txt
setup-dev: setup-env
	python3 -m pip install -r requirements-dev.txt

# ---------------------------------------------------------------------------------------------------------------------
# Generate documentation
# ---------------------------------------------------------------------------------------------------------------------
generate-docs:
	python3 ./generate_schema.py
