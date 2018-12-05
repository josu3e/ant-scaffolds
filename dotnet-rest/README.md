Scaffold para MicroServicio
============================
Microservicio en RestFull que permite la implementación

¿Que incluye?
--------------
* source Code (directory app)
* sam.yaml (directory cloudformation)
* Dockerfile (directory docker/dev, docker/latest)
* Jenkinsfile
* Makefiles (makefile, deploy-aws.mk)

Requerimientos
--------------
* Docker
* Docker Compose
* Cmake

Help
----
* make
* make help

Comandos
--------
```console
Target                        Help                                                       Usage
------                        ----                                                       -----
batch.delete.image.aws.ecr    Eliminar imagenes de docker del repositorio                make batch.delete.image.aws.ecr
build.last                    Construir imagen para deploy                               make build-last
build                         Construir imagen para development                          make build
create.repository.aws.ecr     Crear repositorio en ecr de aws                            create.repository.aws.ecr
deregister.task.definitions   Eliminar tasks definition                                  make deregister.task.definitions
login.aws.ecr                 Login en ecr de aws                                        make login.aws.ecr
logs                          Show container logs                                        make logs
push.aws.ecr                  Publicar imagen en ecr de aws                              make push.aws.ecr
register.task.definition.ecr  Registrando nuevo TaskDefinition                           make register.task.definition.ecr
release                       Construir relaese para produccion                          make release
ssh                           Conectar al container por el protocolo ssh                 make ssh
status                        Show containers status                                     make status
stop                          Stops and removes the docker containers, use me with       make down
up                            up docker containers                                       make up
update.service.ecr            Actualizar Servicio                                        make update.service.cluster
```

Estructura del proyecto
=======================

Directorio de la Aplicacion
---------------------------
```console
app
└── src
```

Deploy de forma manual 
======================
Para hacer deploy del microservicio de forma, usar los siguientes comandos:

```console
~/$ make login.aws.ecr
~/$ make create.repository.aws.ecr
~/$ make build.latest
~/$ make push.aws.ecr
~/$ make update.service.ecr
```
Esto se despliega por defecto en el ambiente de lab (Tokyo).

**NOTE:**
Se debe construir la imagen del contenedor de docker cuando no exista en el repositorio local de docker del equipo o cuando se realize un cambio en el archivo Dockerfile, usando el siguiente comando:
```console
~/$ make build
```

Archivo de configuracion - appsettings.json
===========================================
El archivo de configuracion appsettings.json se debe almacenar en el bucket S3 correspondiente al ambiente de despliegue (dev/pre/prod). Como se muestra a continuacion para el ambiente: dev

```console
s3://infraestructura.dev/config/container/pagoefectivo/dev/custompayment/
```

Para realizar el upload del archivo appsettings.json puede usar el siguiente comando:
```console
aws s3 cp ./appsettings.json s3://infraestructura.dev/config/container/pagoefectivo/dev/custompayment/appsettings.json
```