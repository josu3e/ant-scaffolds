# -*- coding: utf-8 -*-
import dependency_injector.containers as containers
import dependency_injector.providers as providers

from {{ package }}.application.services.example import ExampleAppService
from {{ package }}.domain.services.example import ExampleDomainService
from {{ package }}.infrastructure.repository.mockup.example import MockExampleRepository
from {{ package }}.infrastructure.repository.sqlalchemy.example import ExampleSqlAlchemyRepository


class RepositoryInjector(containers.DeclarativeContainer):
    example = providers.Singleton(ExampleSqlAlchemyRepository)


class DomainServiceInjector(containers.DeclarativeContainer):
    example = providers.Singleton(ExampleDomainService, repository=RepositoryInjector.example)


class AppServiceInjector(containers.DeclarativeContainer):
    example = providers.Singleton(ExampleAppService, domain_service=DomainServiceInjector.example)


'''
Mock Class
'''


class MockRepositoryInjector(containers.DeclarativeContainer):
    example = providers.Factory(MockExampleRepository)


class MockDomainServiceInjector(containers.DeclarativeContainer):
    example = providers.Factory(ExampleDomainService, repository=MockRepositoryInjector.example)


class MockAppServiceInjector(containers.DeclarativeContainer):
    example = providers.Singleton(ExampleAppService, domain_service=MockDomainServiceInjector.example)
