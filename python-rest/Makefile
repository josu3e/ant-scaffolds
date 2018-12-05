.DEFAULT_GOAL := help

## General vars ##
SERVICE_NAME 	= {{ package }}
PATH_PREFIX 	= /{{ api_version }}
CONTAINER_PORT  = {{ container_port }}
TAG_DEV			= dev

## Result vars ##
PROJECT_NAME	= $(SERVICE_NAME)Project
CONTAINER_NAME 	= $(PROJECT_NAME)_backend
IMAGE_DEV		= $(PROJECT_NAME):$(TAG_DEV)

## Target Dev ##

build: ## build image to dev: make build
	cp app/requirements.txt docker/dev/resources/requirements.txt
	docker build -f docker/dev/Dockerfile -t $(IMAGE_DEV) docker/dev/
	rm -f docker/dev/resources/requirements.txt

up: ## up docker containers: make up
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	CONTAINER_PORT=$(CONTAINER_PORT) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
  	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(PROJECT_NAME) up -d
	@make status

down: ## Stops and removes the docker containers: make down
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	CONTAINER_PORT=$(CONTAINER_PORT) \
  	VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(PROJECT_NAME) down

status: ## Show containers status: make status
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	CONTAINER_PORT=$(CONTAINER_PORT) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(PROJECT_NAME) ps

stop: ## Stops and removes the docker containers, use me with: make down
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	CONTAINER_PORT=$(CONTAINER_PORT) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(PROJECT_NAME) stop

restart: ## Restart all containers, use me with: make restart
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	CONTAINER_PORT=$(CONTAINER_PORT) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(PROJECT_NAME) restart
	@make status

ssh: ## Connect to container for ssh protocol
	docker exec -it $(CONTAINER_NAME) bash

log: ## Show container logs
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	CONTAINER_PORT=$(CONTAINER_PORT) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(PROJECT_NAME) logs -f

install-lib: ## Connect to container for ssh protocol install with pip: make install-lib
	docker exec -it $(CONTAINER_NAME) pip-3.5 install $(LIB)

tests: ## Run the unitTests
	@docker run --rm -t -v $(PWD)/app:/app:rw --entrypoint /resources/test.sh $(IMAGE_DEV)

## Target Help ##

help:
	@printf "\033[31m%-16s %-59s %s\033[0m\n" "Target" "Help" "Usage"; \
	printf "\033[31m%-16s %-59s %s\033[0m\n" "------" "----" "-----"; \
	grep -hE '^\S+:.*## .*$$' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' | sort | awk 'BEGIN {FS = ":"}; {printf "\033[32m%-16s\033[0m %-58s \033[34m%s\033[0m\n", $$1, $$2, $$3}'
