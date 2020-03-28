.PHONY: build tests
.ONSHELL:


env=$$PWD/env/bin
python=$(env)/python
git_branch=$(shell git rev-parse --abbrev-ref HEAD)
git_version=$(shell git rev-parse --abbrev-ref HEAD | cut -b 9-)
pypi_url=https://test.pypi.org/legacy/

ifeq ($(pypi),production)
	pypi_url=https://upload.pypi.org/legacy/
endif

# Building
# -----------------------------------------------------------------------------

lint=$(env)/flake8
lint_args=--builtins=ModuleNotFoundError
build_mode=bdist_wheel

build:
ifeq ($(shell $(lint) harvest $(lint_args)),)
	$(python) setup.py $(build_mode)
else
	@$(lint) harvest $(lint_args)
endif

test:
	$(python) -m unittest tests

publish: build
	git push origin $(git_branch)
	twine upload \
		--repository-url $(pypi_url) \
		dist/harvest_api-$(git_version)-py3-none-any.whl
