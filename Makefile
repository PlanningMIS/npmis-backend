# Makefile for managing Django development tasks

# Variables
SETTINGS = --settings=config.settings.dev
APP_TEMPLATE = ../templates/app_template  # Path to your custom app template
# Default target
.PHONY: help
help:
	@echo Available commands
	@echo - start: Start the development server
	@echo - startapp: Create a new app
	@echo - migrate: Apply migrations
	@echo - makemigrations: Create migrations
	@echo - dbshell: Open the database shell
	@echo - shell: Open the Python shell
	@echo - shell-plus: Open the enhanced Python shell
	@echo - install: Install development dependencies
	@echo - test: Run tests

# Start the development server
.PHONY: runserver
runserver:
	python manage.py runserver $(SETTINGS)

# Create a new app (use with: make startapp <app_name>)
.PHONY: startapp
startapp:
	cd apps && python ../manage.py startapp $(word 2, $(MAKECMDGOALS)) --template=$(APP_TEMPLATE) --name=apps.py --name=__init__.py --name=views.py $(SETTINGS)
# Apply migrations
.PHONY: migrate
migrate:
	python manage.py migrate $(SETTINGS)

# Create migrations
.PHONY: makemigrations
makemigrations:
	python manage.py makemigrations $(SETTINGS)

# Open the database shell
.PHONY: dbshell
dbshell:
	python manage.py dbshell $(SETTINGS)

# Open the Python shell
.PHONY: shell
shell:
	python manage.py shell $(SETTINGS)

# Open the enhanced Python shell
.PHONY: shell-plus
shell-plus:
	python manage.py shell_plus $(SETTINGS)

# Install development dependencies
.PHONY: install
install:
	pip install -r requirements/dev.txt

# Run tests
.PHONY: test
test:
	python manage.py test $(SETTINGS)

# Prevent conflicts with Makefile targets
%:
	@: