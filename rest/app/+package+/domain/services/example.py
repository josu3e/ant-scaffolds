# -*- coding: utf-8 -*-


class {{ resource }}DomainService(object):

    def __init__(self, repository):
        self.repository = repository

    def find_by_id(self, id):
        return self.repository.find_by_id(id)

    def find_all(self):
        return self.repository.find_all()

    def create(self, {{ resource_name }}_entity):
        return self.repository.create({{ resource_name }}_entity)

    def update(self, id, {{ resource_name }}_entity):
        return self.repository.update(id, {{ resource_name }}_entity)

    def delete(self, id):
        return self.repository.delete(id)
