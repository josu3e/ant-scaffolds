.DEFAULT_GOAL := help

## GENERAL ##
OWNER 			= {{ product_name }}
SERVICE_NAME 	= {{ package }}
PATH_PREFIX 	= {{ api_version }}

## DEV ##
TAG_DEV			= dev
TAG_CLI 		= cli

## DEPLOY ##
ENV 			?= dev
BUILD_NUMBER 	?= 000006
BUILD_TIMESTAMP ?= 20181004
DEPLOY_REGION 	?= eu-west-1
ACCOUNT_ID		?= 929226109038
DESIRED_COUNT 	?= 1
MIN_SCALING		?= 1
MAX_SCALING		?= 2
HTTPS_PRIORITY 	?= 41
MEMORY_SIZE 	?= 128
CONTAINER_PORT 	?= 8080
INFRA_BUCKET 	?= infraestructura.$(ENV)
SLACK_CHANNEL   ?= $(OWNER)-$(ENV)-changelog
SLACK_WEB_HOOK ?= {{ slack_web_hook }}

## RESULT_VARS ##
DEV_REGISTRY 	= local.$(OWNER).registry:5000
DOCKER_NETWORK 	= $(OWNER)_network
LOCAL_PROJECT_NAME	= $(OWNER)$(ENV)$(SERVICE_NAME)
PROJECT_NAME	= $(OWNER)-$(ENV)-$(SERVICE_NAME)
CONTAINER_NAME 	= $(PROJECT_NAME)_backend
IMAGE_DEV		= $(PROJECT_NAME):$(TAG_DEV)
IMAGE_CLI		= $(PROJECT_NAME):$(TAG_CLI)
TAG_DEPLOY		= $(BUILD_TIMESTAMP).$(BUILD_NUMBER)
IMAGE_DEPLOY	= $(PROJECT_NAME):$(TAG_DEPLOY)
CLUSTER 		= $(OWNER)-$(ENV)
DEPLOY_REGISTRY = $(ACCOUNT_ID).dkr.ecr.$(DEPLOY_REGION).amazonaws.com
STACK_PATH		= $(INFRA_BUCKET)/build/cloudformation/$(OWNER)/$(ENV)/$(PROJECT_NAME)
ECS_CLUSTER     ?= $(OWNER)-$(ENV)


## Target Commons ##

build: ## build image to dev: make build
	cp app/requirements.txt docker/dev/resources/requirements.txt
	docker build -f docker/dev/Dockerfile -t $(IMAGE_DEV) docker/dev/
	rm -f docker/dev/resources/requirements.txt

## Target Dev ##

pull: ## pull docker images from local registery: make pull
	docker pull $(DEV_REGISTRY)/$(IMAGE_DEV)
	docker tag $(DEV_REGISTRY)/$(IMAGE_DEV) $(IMAGE_DEV)
	docker rmi $(DEV_REGISTRY)/$(IMAGE_DEV)
	docker pull $(DEV_REGISTRY)/$(IMAGE_DEPLOY)
	docker tag $(DEV_REGISTRY)/$(IMAGE_DEPLOY) $(IMAGE_DEPLOY)
	docker rmi $(DEV_REGISTRY)/$(IMAGE_DEPLOY)

push: ## push docker images to local registry: make push
	docker tag $(IMAGE_DEV) $(DEV_REGISTRY)/$(IMAGE_DEV)
	docker push $(DEV_REGISTRY)/$(IMAGE_DEV)
	docker rmi $(DEV_REGISTRY)/$(IMAGE_DEV)
	docker tag $(IMAGE_DEPLOY) $(DEV_REGISTRY)/$(IMAGE_DEPLOY)
	docker push $(DEV_REGISTRY)/$(IMAGE_DEPLOY)
	docker rmi $(DEV_REGISTRY)/$(IMAGE_DEPLOY)
	docker images

up: ## up docker containers: make up
	@make verify_network &> /dev/null
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	DOCKER_NETWORK=$(DOCKER_NETWORK) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
  DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(LOCAL_PROJECT_NAME) up -d
	@make status

down: ## Stops and removes the docker containers: make down
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	DOCKER_NETWORK=$(DOCKER_NETWORK) \
  VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(LOCAL_PROJECT_NAME) down

status: ## Show containers status: make status
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	DOCKER_NETWORK=$(DOCKER_NETWORK) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(LOCAL_PROJECT_NAME) ps

stop: ## Stops and removes the docker containers, use me with: make down
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	DOCKER_NETWORK=$(DOCKER_NETWORK) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(LOCAL_PROJECT_NAME) stop

restart: ## Restart all containers, use me with: make restart
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	DOCKER_NETWORK=$(DOCKER_NETWORK) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(LOCAL_PROJECT_NAME) restart
	@make status

ssh: ## Connect to container for ssh protocol
	docker exec -it $(CONTAINER_NAME) bash

log: ## Show container logs
	@IMAGE_DEV=$(IMAGE_DEV) \
	CONTAINER_NAME=$(CONTAINER_NAME) \
	DOCKER_NETWORK=$(DOCKER_NETWORK) \
	VIRTUAL_HOST=$(VIRTUAL_HOST) \
	DEPLOY_REGION=$(DEPLOY_REGION) \
	docker-compose -p $(LOCAL_PROJECT_NAME) logs -f

install-lib: ## Connect to container for ssh protocol install with pip: make install-lib
	docker exec -it $(CONTAINER_NAME) pip-3.5 install $(LIB)

tests: ## Run the unitTests
	@docker run --rm -t -v $(PWD)/app:/app:rw --entrypoint /resources/test.sh $(IMAGE_DEPLOY)

verify_network: ## Verify the local network was created in docker: make verify_network
	@if [ -z $$(docker network ls | grep $(DOCKER_NETWORK) | awk '{print $$2}') ]; then\
		(docker network create $(DOCKER_NETWORK));\
	fi

## Deploy ##

sync-cloudformation: ## Sync additional cloudformation resources in S3: make sync-cloudformation
	aws s3 sync ./cloudformation/stacks s3://$(STACK_PATH)

sync-task-definition: ## Sync task definition
	aws s3 sync s3://$(INFRA_BUCKET)/config/container/orbis/base/ app/config/task/

	@sed -i -e 's/ecs.BRANCH_BUILD/${OWNER}.${ENV}/g; s/MS_NAME/${SERVICE_NAME}/g; s/SRV_NAME/ecs/g; s/ECS_PROJECT/${PROJECT_NAME}/g; s/DEPLOY_REGION/${DEPLOY_REGION}/g; s/BUILD_TIMESTAMP/${BUILD_TIMESTAMP}/g; s/BUILD_NUMBER/${BUILD_NUMBER}/g; s/TASK_RAM/${MEMORY_SIZE}/g' app/config/task/task-definition.json

	@cat app/config/task/task-definition.json

sync-config: ## Sync configs files from S3: make sync-config
	aws s3 sync s3://$(INFRA_BUCKET)/config/container/$(OWNER)/$(ENV)/$(SERVICE_NAME)/ app/config/

push-config: ## Sync configs files to push: make sync-config
	aws s3 sync app/config/ s3://$(INFRA_BUCKET)/config/container/$(OWNER)/$(ENV)/$(SERVICE_NAME)/

update-service: ## Deploy service with cloudformation: make update-service
	aws cloudformation deploy \
	--template-file ./cloudformation/master.yml \
	--stack-name $(PROJECT_NAME)-service \
	--parameter-overrides \
		S3Path=$(STACK_PATH) \
		HttpsListenerPriority=$(HTTPS_PRIORITY) \
		DesiredCount=$(DESIRED_COUNT) \
		MaxScaling=$(MAX_SCALING) \
		MinScaling=$(MIN_SCALING) \
		Image=$(DEPLOY_REGISTRY)/$(IMAGE_DEPLOY) \
		ServiceName=$(SERVICE_NAME) \
		Env=$(ENV) \
		Owner=$(OWNER) \
		PathPrefix=$(PATH_PREFIX) \
		ContainerPort=$(CONTAINER_PORT) \
		MemorySize=$(MEMORY_SIZE) \
	--region $(DEPLOY_REGION) \
	--capabilities CAPABILITY_NAMED_IAM

create-registry: ## Create registry in aws ECR service: make create-registry
	aws cloudformation deploy \
	--template-file ./cloudformation/registry.yml \
	--stack-name $(PROJECT_NAME)-registry \
	--parameter-overrides \
		ProjectName=$(PROJECT_NAME) \
	--region $(DEPLOY_REGION) \
	--capabilities CAPABILITY_IAM

install: ## Building images dev: make install
	@make build

deploy: ## Exec all step to deploy microservice in aws: make deploy
	@make install build-latest publish update-service

build-latest: ## Build image to push to aws ECR: make build-latest
	docker build -f docker/latest/Dockerfile --no-cache --build-arg IMAGE=$(IMAGE_DEV) -t $(IMAGE_DEPLOY) .

publish: ## Push image to aws ECR: make publish
	docker tag $(IMAGE_DEPLOY) $(DEPLOY_REGISTRY)/$(IMAGE_DEPLOY)
	aws --region $(DEPLOY_REGION) ecr get-login --no-include-email | sh
	docker push $(DEPLOY_REGISTRY)/$(IMAGE_DEPLOY)

chown: ## change the permission for app
	@sudo chown -R $(USER):$(USER) $(PWD)/app/*

slack-notify: ## Send slack notify
	curl -X POST \
	--data-urlencode 'payload={"channel":"$(SLACK_CHANNEL)","username":"Jenkins", "icon_url":"https://wiki.jenkins.io/download/attachments/2916393/logo.png", "attachments":[{"color":"good","title":"$(SLACK_TITLE)", "title_link":"$(SLACK_LINK)", "text":"$(SLACK_TEXT)"}]}' \
	$(SLACK_WEB_HOOK)

update-ecs:
	aws ecs register-task-definition --cli-input-json file://app/config/task/task-definition.json --region ${DEPLOY_REGION}
	aws ecs update-service --cluster ${ECS_CLUSTER} --service ${PROJECT_NAME} --task-definition ${PROJECT_NAME} --desired-count ${DESIRED_COUNT} --region ${DEPLOY_REGION}

	rm -rf app/config/task/

## Target Help ##

help:
	@printf "\033[31m%-16s %-59s %s\033[0m\n" "Target" "Help" "Usage"; \
	printf "\033[31m%-16s %-59s %s\033[0m\n" "------" "----" "-----"; \
	grep -hE '^\S+:.*## .*$$' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' | sort | awk 'BEGIN {FS = ":"}; {printf "\033[32m%-16s\033[0m %-58s \033[34m%s\033[0m\n", $$1, $$2, $$3}'
