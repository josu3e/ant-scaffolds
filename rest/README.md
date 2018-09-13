
Scaffold para MicroServicio
---------------------------

### Iniciar el proyecto

````bash
> make build
> make build-latests
> make up
````


### Ejecutar los test

````bash
> make tests
````


### Para ver más comandos

````bash
> make
````


### Variables Requeridas

| variable | descripción |
|----------|-------------|
| name | nombre del proyecto |
| product_name | nombre del producto (urbania, neoauto, aptitus, pagoefectivo) |
| package | nombre que tendrá tu paquete principal (project, user, search, etc) |
| api_version | versión de la API que se esta creando |
| container_port | puerto donde escuchara el servicio |
| slack_web_hook | webhook hacia donde jenkins notificara los despliegues |
| https_listener_dev | listener para dev |
| https_listener_pre | listener para pre |
| https_listener_prod | listener para prod |
| vpc_dev | id de la vpc para dev |
| vpc_pre | id de la vpc para pre |
| vpc_prod | id de la vpc para prod |