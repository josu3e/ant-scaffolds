# -*- coding: utf-8 -*-

from bootstrap.container import AppServicesInjector
from bootstrap.container import MockAppServicesInjector
from .base import BaseCollectionHandler, BaseHandler


class HealthCollectionHandler(BaseCollectionHandler):
    service = MockAppServicesInjector.health()


class HealthHandler(BaseHandler):
    service = MockAppServicesInjector.health()
