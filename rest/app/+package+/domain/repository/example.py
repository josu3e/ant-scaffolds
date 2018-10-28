# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class {{ resource }}Repository(ABC):
    @abstractmethod
    def create(self, {{ resource_name }}_entity):
        raise NotImplementedError

    @abstractmethod
    def update(self, id, {{ resource_name }}_entity):
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
