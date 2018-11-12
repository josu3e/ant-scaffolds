# -*- coding: utf-8 -*-

from bootstrap.container import AppServicesInjector
from bootstrap.container import MockAppServicesInjector
from .base import BaseCollectionHandler, BaseHandler


class ExampleCollectionHandler(BaseCollectionHandler):
    service = MockAppServicesInjector.example()


class ExampleHandler(BaseHandler):
    service = MockAppServicesInjector.example()
