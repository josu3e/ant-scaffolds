# -*- coding: utf-8 -*-
from {{ package }}.domain.repository.{{ resource_name }} import {{ resource }}Repository
from {{ package }}.domain.factories.entities.{{ resource_name }} import {{ resource }}Factory
from {{ package }}.domain.entities.{{ resource_name }} import {{ resource }}


class Mock{{ resource }}Repository({{ resource }}Repository):

    def __init__(self):
        self.data = [
            {
                'id': 1, 'name': 'Kalel'
            },
            {
                'id': 2, 'name': 'scaffold'
            },
        ]

    def create(self, {{ resource_name }}):
        self.data.append(
            {
                'id': {{ resource_name }}.id,
                'name': {{ resource_name }}.name,
            }
        )
        return True

    def update(self, {{ resource_name }}):
        pass

    def delete(self, id):
        pass

    def find_all(self):
        resp = []
        for {{ resource_name }} in self.data:
            {{ resource_name }}_entity = {{ resource }}Factory.create(**{{ resource_name }})
            resp.append({'id': {{ resource_name }}_entity.id, 'name': {{ resource_name }}_entity.name})
        return resp

    def find_by_id(self, id):
        for {{ resource_name }} in self.data:
            if {{ resource_name }}['id'] is int(id):
                {{ resource_name }}_entity = {{ resource }}Factory.create(**{{ resource_name }})
                return {'id': {{ resource_name }}_entity.id, 'name': {{ resource_name }}_entity.name}

