.PHONY: login.aws \
		create.repository.aws.ecr \
		build-last \
		push.aws.ecr \
		register.task.definition.ecr \
		update.service.ecr \
		batch.delete.image.aws.ecr \
		deregister.task.definitions

## DEPLOY ##
ACCOUNT_ID 		?= 929226109038
BUILD_TIMESTAMP ?= 20181023
BUILD_NUMBER 	?= 001
BRANCH_BUILD	?= $(shell git branch | grep '*' | awk '{print $$2}')
DEPLOY_REGION   ?= ap-northeast-1
TASK_RAM		?= 256
MS_NAME			?= ${OWNER}
SRV_NAME        ?= ${SERVICE_NAME}
APP_SETTINGS     = "appsettings.json"
MAX_IMAGES_ALLOWED = 5
MAX_TASKDEF_ALLOWED = 5

BUILD_NUMBER_DEPLOY = $(shell echo `printf %03d ${BUILD_NUMBER}`)
TAG_DEPLOY		    = ${BUILD_TIMESTAMP}.${BUILD_NUMBER_DEPLOY}
IMAGE_DEPLOY	    = ${PROJECT_NAME}:${TAG_DEPLOY}
REGISTRY_DEPLOY     = ${ACCOUNT_ID}.dkr.ecr.${DEPLOY_REGION}.amazonaws.com
ECS_CLUSTER		    = ${OWNER}-${ENV}
PATH_TASK_DEF       = ${INFRA_BUCKET}/config/container/orbis/base/task-definition.json
SETTINGS_PATH       = ${INFRA_BUCKET}/config/container/${OWNER}/${ENV}/${SERVICE_NAME}

## FUNCTION ##

define copy_task_definition_from_bucket
	aws s3 cp s3://${PATH_TASK_DEF} ${PWD}/
endef

define update_task_definition
	cat ${PWD}/task-definition.json | \
		sed 's/ecs.BRANCH_BUILD.MS_NAME.SRV_NAME/${SRV_NAME}.${BRANCH_BUILD}.task.${MS_NAME}/g'\
		| sed 's/ECS_PROJECT/${PROJECT_NAME}/g' \
		| sed 's/DEPLOY_REGION/${DEPLOY_REGION}/g' \
		| sed 's/BUILD_TIMESTAMP/${BUILD_TIMESTAMP}/g' \
		| sed 's/BUILD_NUMBER/${BUILD_NUMBER_DEPLOY}/g' \
		| sed 's/TASK_RAM/${TASK_RAM}/g' \
		| sed 's/BRANCH_BUILD/${BRANCH_BUILD}/g' \
		| sed 's/MS_NAME/${MS_NAME}/g' \
		| sed 's/SRV_NAME/${SRV_NAME}/g' >  ${PWD}/task-def-deploy.json
endef

define delete_task_definition
	rm -rf ${PWD}/task-definition.json
endef

define delete_task_def_deploy
	rm -rf ${PWD}/task-def-deploy.json
endef

define get_configs_from_bucket  
	@if [ ${ENV} != 'lab' ]; then \
		@echo "Get appsettings.json..."; \
		aws s3 cp s3://${SETTINGS_PATH}/${APP_SETTINGS} ${PWD}/${APP_DIR}/release/; \
	fi 
endef

## TARGET ##

login.aws.ecr: ## Login en ecr de aws: make login.aws.ecr
	aws ecr \
		get-login \
		--no-include-email\
		--region $(DEPLOY_REGION) | sh

create.repository.aws.ecr: ## Crear repositorio en ecr de aws: create.repository.aws.ecr
	$(eval EXITS_REPOSITORY := $(shell aws ecr \
		describe-repositories \
		--repository-name ${PROJECT_NAME} \
		--region $(DEPLOY_REGION) \
		| grep "repositoryName" \
		| sed 's/repositoryName//g'\
		| sed 's/://g'| sed 's/,//g'| sed 's/ //g'| sed 's/"//g'))
	@if [ "${EXITS_REPOSITORY}" != "${PROJECT_NAME}" ]; then aws ecr create-repository --repository-name ${PROJECT_NAME} --region $(DEPLOY_REGION); fi

build.latest: ## Construir imagen para deploy: make build-latest
	$(call get_configs_from_bucket)
	docker build \
		-f docker/latest/Dockerfile \
		--no-cache \
		-t $(REGISTRY_DEPLOY)/$(IMAGE_DEPLOY) .

push.aws.ecr: ## Publicar imagen en ecr de aws: make push.aws.ecr
	docker push \
		$(REGISTRY_DEPLOY)/$(IMAGE_DEPLOY)

register.task.definition.ecr: ## Registrando nuevo TaskDefinition: make register.task.definition.ecr
	$(call copy_task_definition_from_bucket)
	$(call update_task_definition)
	$(call delete_task_definition)
	aws ecs \
		register-task-definition \
		--cli-input-json \
		file://${PWD}/task-def-deploy.json \
		--region ${DEPLOY_REGION}
	
update.service.ecr: ## Actualizar Servicio: make update.service.cluster
	aws ecs \
		update-service \
		--cluster ${ECS_CLUSTER} \
		--service ${PROJECT_NAME} \
		--task-definition ${PROJECT_NAME} \
		--desired-count 1 \
		--region ${DEPLOY_REGION}

deregister.task.definitions: ## Eliminar tasks definition: make deregister.task.definitions
	$(eval TOTAL_TASKDEF := $(shell aws --region \
								${DEPLOY_REGION} \
								ecs list-task-definitions \
								--sort DESC --family-prefix ${PROJECT_NAME} \
								--output text \
								| cut -d'/' -f2 | wc -l))

	$(info "Total task definition: $(TOTAL_TASKDEF)")
	if [ ${TOTAL_TASKDEF} -gt ${MAX_TASKDEF_ALLOWED} ]; then \
		$(eval FILE_TASKDEF:= $(shell echo '${PWD}/file_taskdef.${BUILD_NUMBER_DEPLOY}')) \
		$(eval TOTAL_LINE:= $(shell echo '${TOTAL_TASKDEF} - ${MAX_TASKDEF_ALLOWED}' | bc)) \
		aws --region \
			${DEPLOY_REGION} \
			ecs list-task-definitions \
			--sort DESC --family-prefix ${PROJECT_NAME} \
			--output text \
			| cut -d'/' -f2 > ${FILE_TASKDEF};\
		\
		for line in `cat ${FILE_TASKDEF} | tail -n ${TOTAL_LINE}`; do \
			aws ecs deregister-task-definition --task-definition $${line}; \
			echo "Deregister task definition: $${line}"; \
		done; \
	fi

	@if [ -f ${FILE_TASKDEF} ]; then \
		rm -rf ${FILE_TASKDEF}; \
	fi

batch.delete.image.aws.ecr: ## Eliminar imagenes de docker del repositorio: make batch.delete.image.aws.ecr
	$(eval TOTAL_IMAGES := $(shell aws --region \
								${DEPLOY_REGION} \
								ecr list-images \
								--repository-name ${PROJECT_NAME} \
								| grep imageTag \
								| cut -d'"' -f4 \
								| sort -rn | wc -l))

	$(info "Total Imagen: $(TOTAL_IMAGES)")
	if [ ${TOTAL_IMAGES} -gt ${MAX_IMAGES_ALLOWED} ]; then \
		$(eval FILE_IMAGES:= $(shell echo '${PWD}/file_images.${BUILD_NUMBER_DEPLOY}')) \
		$(eval TOTAL_LINE:= $(shell echo '${TOTAL_IMAGES} - ${MAX_IMAGES_ALLOWED}' | bc)) \
		aws --region \
			${DEPLOY_REGION} \
			ecr list-images \
			--repository-name ${PROJECT_NAME} \
			| grep imageTag \
			| cut -d'"' -f4 \
			| sort -rn > ${FILE_IMAGES};\
		\
		for line in `cat ${FILE_IMAGES} | tail -n ${TOTAL_LINE}`; do \
			aws ecr batch-delete-image --repository-name ${PROJECT_NAME} --image-ids imageTag=$${line} --region ${DEPLOY_REGION}; \
			echo "Deleting image: $${line}"; \
		done; \
	fi
	
	@if [ -f ${FILE_IMAGES} ]; then \
		rm -rf ${FILE_IMAGES}; \
	fi