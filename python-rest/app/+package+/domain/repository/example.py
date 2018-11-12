# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class ExampleRepository(ABC):
    @abstractmethod
    def create(self, example_entity):
        raise NotImplementedError

    @abstractmethod
    def update(self, id, example_entity):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id):
        raise NotImplementedError

    @abstractmethod
    def find_all(self):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id):
        raise NotImplementedError
