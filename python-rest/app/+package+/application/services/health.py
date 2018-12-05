# -*- coding: utf-8 -*-
from .base import BaseAppService
from {{ package }}.domain.factories.entities.health import HealthFactory
from {{ package }}.infrastructure.helpers.try_except import handler_except


class HealthAppService(BaseAppService):

    def __init__(self, domain_service):
        self.__domain_service = domain_service

    @handler_except
    def find_by_id(self, id):
        result = self.__domain_service.find_by_id(id)
        return result

    @handler_except
    def find_all(self):
        result = self.__domain_service.find_all()
        return result

    @handler_except
    def create(self, **kwargs):
        health_entity = HealthFactory.create(**kwargs)
        result = self.__domain_service.create(health_entity)

    @handler_except
    def update(self, id, **kwargs):
        health_entity = HealthFactory.create(**kwargs)
        result = self.__domain_service.update(id, health_entity)
        return result

    @handler_except
    def delete(self, id):
        result = self.__domain_service.delete(id)
        return result
