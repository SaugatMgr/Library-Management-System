.PHONY: install
install:
	poetry install

# for consistency we uninstall and install hooks in pre-commit
.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: check-all-files
check-all-files:
	poetry run pre-commit run --all-files

.PHONY: runserver
runserver:
	poetry run python -m core.manage runserver

.PHONY: shell
shell:
	poetry run python -m core.manage shell

.PHONY: showmigrations
showmigrations:
	poetry run python -m core.manage showmigrations

.PHONY: makemigrations
makemigrations:
	poetry run python -m core.manage makemigrations

.PHONY: migrate
migrate:
	poetry run python -m core.manage migrate

.PHONY: superuser
superuser:
	poetry run python -m core.manage createsuperuser

.PHONY: setup
setup: install migrate
