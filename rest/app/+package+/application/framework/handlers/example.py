# -*- coding: utf-8 -*-

from bootstrap.container import AppServicesInjector
from bootstrap.container import MockAppServicesInjector
from .base import BaseCollectionHandler, BaseHandler


class {{ resource }}CollectionHandler(BaseCollectionHandler):
    service = MockAppServicesInjector.{{ resource_name }}()


class {{ resource }}Handler(BaseHandler):
    service = MockAppServicesInjector.{{ resource_name }}()
