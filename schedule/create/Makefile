.DEFAULT_GOAL := help

## GENERAL ##
OWNER 			= {{ product_name|lower }}
SERVICE_NAME 	= {{ package|lower }}

## DEV ##
TAG_DEV			= dev
LOCAL_REGISTRY 	= local.$(OWNER).registry:5000
DOCKER_NETWORK 	= $(OWNER)_network

## DEPLOY ##
ENV 			?= dev
INFRA_BUCKET 	?= infraestructura.$(ENV)
ACCOUNT_ID		?= 929226109038
BUILD_NUMBER 	?= 0004
BUILD_TIMESTAMP ?= ${shell date '+%d%m%Y'}
DEPLOY_REGION 	?= eu-west-1
MEMORY_SIZE 	?= 128

## RESULT_VARS ##
PROJECT_NAME	= ${OWNER}-${ENV}-${SERVICE_NAME}
CONTAINER_NAME 	= ${PROJECT_NAME}_backend
IMAGE_DEV		= ${PROJECT_NAME}:${TAG_DEV}
TAG_DEPLOY		= ${BUILD_TIMESTAMP}.${BUILD_NUMBER}
IMAGE_DEPLOY	= ${PROJECT_NAME}:${TAG_DEPLOY}
CLUSTER 		= ${OWNER}-dev
DEPLOY_REGISTRY = ${ACCOUNT_ID}.dkr.ecr.${DEPLOY_REGION}.amazonaws.com
STACK_PATH		= ${INFRA_BUCKET}/build/cloudformation/${OWNER}/${ENV}/${PROJECT_NAME}

## Commons ##
build: ## build image, use me with: make build
	cp app/requirements.txt docker/dev/resources/requirements.txt
	docker build -f docker/dev/Dockerfile -t $(IMAGE_DEV) docker/dev/
	rm -f docker/dev/resources/requirements.txt

## Function Dev ##

pull: ## pull docker images from local Registery, use me with: make pull
	docker pull $(LOCAL_REGISTRY)/$(IMAGE_DEV)
	docker tag $(LOCAL_REGISTRY)/$(IMAGE_DEV) $(IMAGE_DEV)
	docker rmi $(LOCAL_REGISTRY)/$(IMAGE_DEV)
	docker pull $(LOCAL_REGISTRY)/$(IMAGE_DEPLOY)
	docker tag $(LOCAL_REGISTRY)/$(IMAGE_DEPLOY) $(IMAGE_DEPLOY)
	docker rmi $(LOCAL_REGISTRY)/$(IMAGE_DEPLOY)

push: ## pull docker images from local Registry, use me with: make push
	docker tag ${IMAGE_DEV} ${LOCAL_REGISTRY}/${IMAGE_DEV}
	docker push ${LOCAL_REGISTRY}/${IMAGE_DEV}
	docker rmi ${LOCAL_REGISTRY}/${IMAGE_DEV}
	docker tag ${IMAGE_DEPLOY} ${LOCAL_REGISTRY}/${IMAGE_DEPLOY}
	docker push ${LOCAL_REGISTRY}/${IMAGE_DEPLOY}
	docker rmi ${LOCAL_REGISTRY}/${IMAGE_DEPLOY}

verify_network: ## Verify the local network was created in docker, normaly created before up container service: make verify_network
	@if [ -z $$(docker network ls | grep $(DOCKER_NETWORK) | awk '{print $$2}') ]; then\
		(docker network create $(DOCKER_NETWORK));\
	fi

schedules: ## Execute a command e.g: make schedules CMD=example
	docker run -it --rm -v $(PWD)/app/:/app $(IMAGE_DEV) python3 $(SERVICE_NAME)/cli.py $(CMD)

## Deploy ##

install: ## Exec composer-update un cli image: make install
	@make build

sync-cloudformation: ## Sync additional cloudformation resources in S3 before to push image to registry in aws: make sync-cloudformation
	@aws s3 sync ./cloudformation/stacks s3://${STACK_PATH}

build-latest: ## Build image to push to aws ECR: make build-latest
	docker build -f docker/latest/Dockerfile --no-cache --build-arg IMAGE=${IMAGE_DEV} -t ${IMAGE_DEPLOY} .

update-service:
	@make sync-cloudformation
	aws cloudformation deploy \
	--template-file ./cloudformation/master.yml \
	--stack-name ${PROJECT_NAME}-service \
	--parameter-overrides \
		S3Path=${STACK_PATH} \
		Image=${DEPLOY_REGISTRY}/${IMAGE_DEPLOY} \
		ServiceName=${SERVICE_NAME} \
		Env=${ENV} \
		Owner=${OWNER} \
		MemorySize=${MEMORY_SIZE} \
	--region ${DEPLOY_REGION} \
	--capabilities CAPABILITY_NAMED_IAM

deploy: ## Exec all step to deploy microservice in aws: make deploy
	@make sync-config install build-latest publish update-service

publish:
	docker tag ${IMAGE_DEPLOY} ${DEPLOY_REGISTRY}/${IMAGE_DEPLOY}
	aws --region ${DEPLOY_REGION} ecr get-login --no-include-email | sh
	docker push ${DEPLOY_REGISTRY}/${IMAGE_DEPLOY}

create-registry:
	aws cloudformation deploy \
	--template-file ./cloudformation/registry.yml \
	--stack-name ${PROJECT_NAME}-registry \
	--parameter-overrides \
		ProjectName=$(PROJECT_NAME) \
	--region $(DEPLOY_REGION) \
	--capabilities CAPABILITY_IAM

## Help ##
help:
	@printf "\033[31m%-16s %-59s %s\033[0m\n" "Target" "Help" "Usage"; \
	printf "\033[31m%-16s %-59s %s\033[0m\n" "------" "----" "-----"; \
	grep -hE '^\S+:.*## .*$$' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' | sort | awk 'BEGIN {FS = ":"}; {printf "\033[32m%-16s\033[0m %-58s \033[34m%s\033[0m\n", $$1, $$2, $$3}'
