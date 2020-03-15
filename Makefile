.PHONY: build tests
.ONSHELL:


env=$$PWD/env/bin
python=$(env)/python


# Building
# -----------------------------------------------------------------------------

lint=$(env)/flake8
lint_args=--builtins=ModuleNotFoundError
build_mode=sdist bdist_wheel

build:
ifeq ($(shell $(lint) harvest $(lint_args)),)
	$(python) setup.py $(build_mode)
else
	@$(lint) harvest $(lint_args)
endif

test:
	$(python) -m unittest tests
	