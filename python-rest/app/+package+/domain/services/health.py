# -*- coding: utf-8 -*-


class HealthDomainService(object):

    def __init__(self, repository):
        self.repository = repository

    def find_by_id(self, id):
        return self.repository.find_by_id(id)

    def find_all(self):
        return self.repository.find_all()

    def create(self, health_entity):
        return self.repository.create(health_entity)

    def update(self, id, health_entity):
        return self.repository.update(id, health_entity)

    def delete(self, id):
        return self.repository.delete(id)
