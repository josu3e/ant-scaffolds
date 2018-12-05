# -*- coding: utf-8 -*-
from {{ package }}.domain.entities.health import Health


class HealthFactory():
    @staticmethod
    def create(**kwargs):
        return Health(**kwargs)
