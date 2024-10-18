# ENV defaults to local (so that requirements/local.txt are installed), but can be overridden
#  (e.g. ENV=production make setup).
ENV ?= local
# PYTHON specifies the python binary to use when creating virtualenv
PYTHON ?= python3.6.2

# Editor can be defined globally but defaults to nano
EDITOR ?= nano

# By default we open the editor after copying settings, but can be overridden
#  (e.g. EDIT_SETTINGS=no make settings).
EDIT_SETTINGS ?= yes

# Get root dir and project dir
PROJECT_ROOT ?= $(PWD)
SITE_ROOT ?= $(PROJECT_ROOT)

BLACK ?= \033[0;30m
RED ?= \033[0;31m
GREEN ?= \033[0;32m
YELLOW ?= \033[0;33m
BLUE ?= \033[0;34m
PURPLE ?= \033[0;35m
CYAN ?= \033[0;36m
GRAY ?= \033[0;37m
COFF ?= \033[0m


VERSION=0.7.26
DOCKER_COMPOSE_PROJECT_NAME=133t
DOCKER_COMPOSE=docker-compose -p $(DOCKER_COMPOSE_PROJECT_NAME)
PUBLIC_DOCKER_IMAGE=dvscore/133t
STACK=nginx postgres django
deploy_template= \
	docker push $(PUBLIC_DOCKER_IMAGE):$(VERSION)-$(1);

# Mark non-file targets as PHONY
.PHONY: all help
.PHONY: init-dev build-dev down-dev pull-dev start-dev migrate-dev logs-dev createsuperuser-dev
.PHONY: dropdb-dev createdb-dev generate-demo-dev recreatedb-dev recreatedb-demo-dev
.PHONY: build-prod down-prod pull-prod start-prod migrate-prod logs-prod createsuperuser-prod
.PHONY: dropdb-prod createdb-prod generate-demo-prod recreatedb-prod recreatedb-demo-prod

all: help


help:
	@echo "+------<<<<                                 Configuration                                >>>>------+"
	@echo ""
	@echo "ENV: $(ENV)"
	@echo "PYTHON: $(PYTHON)"
	@echo "PROJECT_ROOT: $(PROJECT_ROOT)"
	@echo "SITE_ROOT: $(SITE_ROOT)"
	@echo ""
	@echo "+------<<<<                                     Tasks                                    >>>>------+"
	@echo ""
	@echo "$(CYAN)make init-dev$(COFF)    - Init Env for Local Development Environment"
	@echo ""
	@echo "$(CYAN)make build-dev$(COFF)    - Build Local Development Environment"
	@echo ""
	@echo "$(CYAN)make down-dev$(COFF)  - Down All Local Development containers"
	@echo ""
	@echo "$(CYAN)make pull-dev$(COFF)     - Pull all Local Development containers"
	@echo ""
	@echo "$(CYAN)make start-dev$(COFF) - Start all Local Development containers"
	@echo ""
	@echo "$(CYAN)make migrate-dev$(COFF)  - Run Django migrations on Local Development containers"
	@echo ""
	@echo "$(CYAN)make logs-dev$(COFF) - Tail Local Development containers logs"
	@echo ""
	@echo "$(CYAN)make build-prod$(COFF)    - Build Production Environment"
	@echo ""
	@echo "$(CYAN)make down-prod$(COFF)  - Down All Production containers"
	@echo ""
	@echo "$(CYAN)make pull-prod$(COFF)     - Pull all Production containers"
	@echo ""
	@echo "$(CYAN)make start-prod$(COFF) - Start all Production containers"
	@echo ""
	@echo "$(CYAN)make migrate-prod$(COFF)  - Run Django migrations on Production containers"
	@echo ""
	@echo "$(CYAN)make logs-prod$(COFF) - Tail Production containers logs"
	@echo ""


init-dev:
	cp -R .envs_example .envs

build-dev:
	docker-compose -f local.yml build

down-dev:
	docker-compose -f local.yml down --remove-orphans

pull-dev:
	docker-compose -f local.yml pull

start-dev:
	docker-compose -f local.yml up -d

migrate-dev:
	docker-compose -f local.yml exec django /entrypoint -- ./manage.py migrate $(cmd)

logs-dev:
	docker-compose -f local.yml logs -f --tail="10"

createsuperuser-dev:
	docker-compose -f local.yml exec django /entrypoint -- python manage.py createsuperuser

dropdb-dev:
	docker volume rm 133t_local_postgres_data

createdb-dev:
	docker-compose -f local.yml run --rm django /entrypoint -- python manage.py migrate

generate-demo-dev:
	docker-compose -f local.yml run --rm django /entrypoint -- ./manage.py generatedemodata

recreatedb-dev: down-dev dropdb-dev createdb-dev
	make down-dev
	make start-dev

recreatedb-demo-dev: down-dev dropdb-dev createdb-dev generate-demo-dev
	make down-dev
	make start-dev

clear-stripe-dev:
	docker-compose -f local.yml exec django /entrypoint -- python manage.py clear_stripe_data

init-stripe-dev:
	docker-compose -f local.yml exec django /entrypoint -- python manage.py init_default_stripe_plans

sync-stripe-dev:
	docker-compose -f local.yml exec django /entrypoint -- python manage.py sync_stripe_plans

create-stripe-dev:
	make clear-stripe-dev
	make init-stripe-dev
	make sync-stripe-dev

set-socials-dev:
	docker-compose -f local.yml exec django /entrypoint -- python manage.py set_social_appid_and_secret

ssh-agent-prod:
	eval "$(ssh-agent -s)"
	ssh-add -K ~/.ssh/one33t.pem

build-prod:
	docker-compose -f production.yml build --build-arg BUILD_ENVIRONMENT=production

down-prod:
	docker-compose -f production.yml down --remove-orphans

pull-prod:
	docker-compose -f production.yml pull

start-prod:
	docker-compose -f production.yml up -d

migrate-prod:
	docker-compose -f production.yml exec django /entrypoint -- ./manage.py migrate $(cmd)

.PHONY: upload-compose-prod
docker-pull-prod:
	docker-compose -f production.yml pull

logs-prod:
	docker-compose -f production.yml logs -f --tail="10"

createsuperuser-prod:
	docker-compose -f production.yml exec django /entrypoint -- python manage.py createsuperuser

dropdb-prod:
	docker volume rm 133t_production_postgres_data

createdb-prod:
	docker-compose -f production.yml run --rm django /entrypoint -- python manage.py migrate

generate-demo-prod:
	docker-compose -f production.yml run --rm django /entrypoint -- ./manage.py generatedemodata

recreatedb-prod: down-prod dropdb-prod createdb-prod
	make down-prod
	make start-prod

recreatedb-demo-prod: down-prod dropdb-prod createdb-prod generate-demo-prod
	make down-prod
	make start-prod

clear-stripe-prod:
	docker-compose -f production.yml exec django /entrypoint -- python manage.py clear_stripe_data

init-stripe-prod:
	docker-compose -f production.yml exec django /entrypoint -- python manage.py init_default_stripe_plans

sync-stripe-prod:
	docker-compose -f production.yml exec django /entrypoint -- python manage.py sync_stripe_plans

create-stripe-prod:
	make clear-stripe-prod
	make init-stripe-prod
	make sync-stripe-prod

set-socials-prod:
	docker-compose -f production.yml exec django /entrypoint -- python manage.py set_social_appid_and_secret


build-test:
	docker-compose -f test.yml build

down-test:
	docker-compose -f test.yml down --remove-orphans

start-test:
	docker-compose -f test.yml up -d

logs-test:
	docker-compose -f test.yml logs -f --tail="10"

frontend-all-test:
	docker-compose -f test.yml exec -T node npm install
	docker-compose -f test.yml exec -T node ./run_tests.sh

backend-all-test:
	docker-compose -f test.yml exec -T django pip install -r requirements/teamcity.txt
	docker-compose -f test.yml exec -T django /entrypoint -- /bin/sh tests/run.sh

.PHONY: release
release: build-prod
	$(foreach service,$(STACK),$(call deploy_template,$(service)))