# -*- coding: utf-8 -*-
from {{ package }}.domain.entities.example import Example


class ExampleFactory():
    @staticmethod
    def create(**kwargs):
        return Example(**kwargs)
