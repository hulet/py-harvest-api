.PHONY: tests
.ONSHELL:
.PHONY: build

project=harvest
loglevel=DEBUG
env=$$PWD/env/bin
python=$(env)/python
version=$(shell cd $(project) && python __init__.py)

# Building
# -----------------------------------------------------------------------------
lint=$(env)/flake8
lint_args=--builtins=ModuleNotFoundError
#build_mode=bdist_wheel
build_mode=sdist

build:
ifeq ($(shell $(lint) harvest $(lint_args)),)
	$(python) setup.py $(build_mode)
else
	@$(lint) harvest $(lint_args)
endif

test:
	export HARVEST_PA_ACCOUNT_ID=your_personalaccount_id
	export HARVEST_PA_TOKEN=your_personalaccount_token
	$(python) -m unittest tests
	