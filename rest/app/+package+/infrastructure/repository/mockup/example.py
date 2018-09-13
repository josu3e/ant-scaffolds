# -*- coding: utf-8 -*-
from {{ package }}.domain.repository.example import ExampleRepository
from {{ package }}.domain.factories.entities.example import ExampleFactory
from {{ package }}.domain.entities.example import Example


class MockExampleRepository(ExampleRepository):

    def __init__(self):
        self.data = [
            {
                'id': 1, 'name': 'Kalel'
            },
            {
                'id': 2, 'name': 'scaffold'
            },
        ]

    def create(self, example):
        self.data.append(
            {
                'id': example.id,
                'name': example.name,
            }
        )
        return True

    def update(self, project):
        pass

    def delete(self, id):
        pass

    def find_all(self):
        resp = []
        for example in self.data:
            example_entity = ExampleFactory.create(**example)
            resp.append({'id': example_entity.id, 'name': example_entity.name})
        return resp

    def find_by_id(self, id):
        for example in self.data:
            if example['id'] is int(id):
                example_entity = ExampleFactory.create(**example)
                return {'id': example_entity.id, 'name': example_entity.name}
