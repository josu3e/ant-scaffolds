# -*- coding: utf-8 -*-
import dependency_injector.containers as containers
import dependency_injector.providers as providers

from {{ package }}.application.services.example import ExampleAppService
from {{ package }}.domain.services.example import ExampleDomainService
from {{ package }}.infrastructure.repository.mockup.example import MockExampleRepository
from {{ package }}.infrastructure.repository.sqlalchemy.example import ExampleSqlAlchemyRepository


class RepositoryInjector(containers.DeclarativeContainer):
    example = providers.Singleton(ExampleSqlAlchemyRepository)


class DomainServicesInjector(containers.DeclarativeContainer):
    example = providers.Singleton(ExampleDomainService, repository=RepositoryInjector.example)


class AppServicesInjector(containers.DeclarativeContainer):
    example = providers.Singleton(ExampleAppService, domain_service=DomainServicesInjector.example)


'''
Mock Class
'''


class MockRepositoryInjector(containers.DeclarativeContainer):
    example = providers.Factory(MockExampleRepository)


class MockDomainServicesInjector(containers.DeclarativeContainer):
    example = providers.Factory(ExampleDomainService, repository=MockRepositoryInjector.example)


class MockAppServicesInjector(containers.DeclarativeContainer):
    example = providers.Singleton(ExampleAppService, domain_service=MockDomainServicesInjector.example)
