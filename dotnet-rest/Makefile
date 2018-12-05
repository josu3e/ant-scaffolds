.DEFAULT_GOAL := help

include makefiles/deploy-aws.mk

## GENERAL ##
OWNER 			= {{ product_name }}
SERVICE_NAME 	= {{ server_name }}
APP_DIR         = app

ENV             ?= lab
INFRA_BUCKET    ?= infraestructura.dev
SLACK_CHANNEL   ?= pe-${ENV}-changelog

## RESULT_VARS ##
PROJECT_NAME     = ${OWNER}-${ENV}-${SERVICE_NAME}
export IMAGE_DEV = ${PROJECT_NAME}:dev

define delete_directory_release
	@if [ -d ${PWD}/${APP_DIR}/release ]; then \
		rm -rf ${PWD}/${APP_DIR}/release; \
	fi
endef

##################################################################
#### Development Commands
##################################################################

ssh: ## Conectar al container por el protocolo ssh: make ssh
	@docker container run \
		--workdir "/${APP_DIR}" \
		--rm \
		-it \
		-p 5000:5000 \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		${IMAGE_DEV} "sh"

build: ## Construir imagen para development: make build
	@docker build \
		-f docker/dev/Dockerfile \
		-t $(IMAGE_DEV) \
		docker/dev/ \
		--no-cache

release: ## Construir relaese para produccion: make release
	$(call delete_directory_release)
	@docker container run \
		--workdir "/${APP_DIR}" \
		--rm \
		-it \
		-v "${PWD}/${APP_DIR}":/${APP_DIR} \
		--tty=false \
		${IMAGE_DEV} \
		dotnet publish /${APP_DIR}/src/app.csproj -o /${APP_DIR}/release

up:  ## up docker containers: make up
	@docker-compose up -d

status: ## Show containers status: make status
	@docker-compose ps

stop: ## Stops and removes the docker containers, use me with: make down
	@docker-compose stop

logs: ## Show container logs: make logs
	@docker-compose logs -f $(IMAGE)

## Target Help ##

help:
	@printf "\033[31m%-28s %-59s %s\033[0m\n" "Target" " Help" "Usage"; \
	printf "\033[31m%-28s %-59s %s\033[0m\n"  "------" " ----" "-----"; \
	grep -hE '^\S+:.*## .*$$' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' | sort | awk 'BEGIN {FS = ":"}; {printf "\033[32m%-28s\033[0m %-58s \033[34m%s\033[0m\n", $$1, $$2, $$3}'
