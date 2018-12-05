# -*- coding: utf-8 -*-
from {{ package }}.domain.repository.health import HealthRepository
from {{ package }}.domain.factories.entities.health import HealthFactory


class MockHealthRepository(HealthRepository):

    def __init__(self):
        self.data = [
            {
                'status': 'OK'
            }
        ]

    def create(self, health):
        pass

    def update(self, health):
        pass

    def delete(self, id):
        pass

    def find_by_id(self, id):
        pass

    def find_all(self):
        resp = []
        for health in self.data:
            health_entity = HealthFactory.create(**health)
            resp.append({'status': health_entity.status})
        return resp
