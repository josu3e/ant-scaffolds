# -*- coding: utf-8 -*-


class ExampleDomainService(object):

    def __init__(self, repository):
        self.repository = repository

    def find_by_id(self, id):
        return self.repository.find_by_id(id)

    def find_all(self):
        return self.repository.find_all()

    def create(self, example_entity):
        return self.repository.create(example_entity)

    def update(self, id, example_entity):
        return self.repository.update(id, example_entity)

    def delete(self, id):
        return self.repository.delete(id)
