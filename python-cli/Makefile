.DEFAULT_GOAL := help
.PHONY : schedules

## GENERAL ##
SERVICE_NAME 	= $(basename pwd)

## DEV ##
TAG_DEV			= dev

## RESULT_VARS ##
PROJECT_NAME	= ${SERVICE_NAME}_project
CONTAINER_NAME 	= ${PROJECT_NAME}_backend
IMAGE_DEV		= ${PROJECT_NAME}:${TAG_DEV}

## Function Dev ##

build: ## build image, use me with: make build
	docker build -f docker/dev/Dockerfile -t $(IMAGE_DEV) docker/dev/

execute: ## Execute a command e.g: make schedules CMD=example
	@docker run -it --rm -v $(PWD):/app $(IMAGE_DEV) $(CMD)

## Help ##
help:
	@printf "\033[31m%-16s %-59s %s\033[0m\n" "Target" "Help" "Usage"; \
	printf "\033[31m%-16s %-59s %s\033[0m\n" "------" "----" "-----"; \
	grep -hE '^\S+:.*## .*$$' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' | sort | awk 'BEGIN {FS = ":"}; {printf "\033[32m%-16s\033[0m %-58s \033[34m%s\033[0m\n", $$1, $$2, $$3}'
