# -*- coding: utf-8 -*-

from {{ package }}.domain.repository.{{ resource_name }} import {{ resource }}Repository
from {{ package }}.domain.entities.{{ resource_name }} import {{ resource }}


class {{ resource }}SqlAlchemyRepository({{ resource }}Repository):

    def __init__(self):
        self.entity = {{ resource }}

    def create(self, {{ resource_name }}_entity):
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
