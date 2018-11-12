# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class BaseAppService(ABC):

    @abstractmethod
    def find_all(self, params):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    def create(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, id, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, id):
        raise NotImplementedError
