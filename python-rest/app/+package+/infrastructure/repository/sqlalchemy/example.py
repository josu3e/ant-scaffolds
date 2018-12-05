# -*- coding: utf-8 -*-

from {{ package }}.domain.repository.example import ExampleRepository
from {{ package }}.domain.entities.example import Example


class ExampleSqlAlchemyRepository(ExampleRepository):

    def __init__(self):
        self.entity = Example

    def create(self, example_entity):
        try:
            pass
        except Exception as e:
            raise e

    def update(self, id, **kwargs):
        try:
            pass
        except Exception as e:
            raise e

    def delete(self, id):
        try:
            pass
        except Exception as e:
            raise e

    def find_all(self):
        try:
            pass
        except Exception as e:
            raise e

    def find_by_id(self, id):
        try:
            pass
        except Exception as e:
            raise e
