# -*- coding: utf-8 -*-
import dependency_injector.containers as containers
import dependency_injector.providers as providers

from {{ package }}.application.services.health import HealthAppService
from {{ package }}.domain.services.health import HealthDomainService
from {{ package }}.infrastructure.repository.mockup.health import MockHealthRepository


class RepositoryInjector(containers.DeclarativeContainer):
    health = providers.Singleton(MockHealthRepository)


class DomainServicesInjector(containers.DeclarativeContainer):
    health = providers.Singleton(HealthDomainService, repository=RepositoryInjector.health)


class AppServicesInjector(containers.DeclarativeContainer):
    health = providers.Singleton(HealthAppService, domain_service=DomainServicesInjector.health)


'''
Mock Class
'''


class MockRepositoryInjector(containers.DeclarativeContainer):
    health = providers.Factory(MockHealthRepository)


class MockDomainServicesInjector(containers.DeclarativeContainer):
    health = providers.Factory(HealthDomainService, repository=MockRepositoryInjector.health)


class MockAppServicesInjector(containers.DeclarativeContainer):
    health = providers.Singleton(HealthAppService, domain_service=MockDomainServicesInjector.health)
