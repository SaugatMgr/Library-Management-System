.PHONY: install
install:
	poetry install

# for consistency we uninstall and install hooks in pre-commit
.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall && poetry run pre-commit install

.PHONY: clear-cache
clear-cache:
	poetry run pre-commit clean

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

# Celery Commands
.PHONY: celery
celery:
	poetry run celery -A core.LibraryMgmtSys worker -l info

.PHONY: celery-beat
celery-beat:
	poetry run celery -A core.LibraryMgmtSys beat -l info

# Docker commands
.PHONY: compose-up
compose-up:
	poetry run docker-compose up

.PHONY: compose-down
compose-down:
	poetry run docker-compose down

.PHONY: compose-build
compose-build:
	poetry run docker-compose build

.PHONY: rebuild
rebuild:
	poetry run docker-compose down && poetry run docker-compose build && poetry run docker-compose up

.PHONY: compose-d
compose-d:
	poetry run docker-compose up -d

.PHONY: compose-logs
compose-logs:
	poetry run docker-compose logs -f

.PHONY: compose-stop
compose-stop:
	poetry run docker-compose stop

# remove all both running/stopped images, -q list only ids, -f specifies force remove
.PHONY: rm-images
rm-images:
	poetry run docker rmi $(poetry run docker images -q) -f

# remove all both running/stopped containers, -a means all, -q list only ids, -f specifies force remove
.PHONY: rm-containers
rm-containers:
	poetry run docker rm $(poetry run docker ps -a -q) -f

# remove all both running/stopped volumes, -q list only ids, -f specifies force remove
.PHONY: rm-volumes
rm-volumes:
	poetry run docker volume rm $(poetry run docker volume ls -q) -f
