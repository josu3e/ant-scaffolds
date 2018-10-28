# -*- coding: utf-8 -*-
from {{ package }}.domain.entities.{{ resource_name }} import {{ resource }}


class {{ resource }}Factory():
    @staticmethod
    def create(**kwargs):
        return {{ resource }}(**kwargs)
