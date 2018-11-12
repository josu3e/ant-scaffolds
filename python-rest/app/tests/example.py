# -*- coding: utf-8 -*-

import unittest

from bootstrap.container import MockAppServicesInjector


class ExampleTestCase(unittest.TestCase):
    def setUp(self):
        self.service = MockAppServicesInjector.example()

    def example_test_1_find_all(self):
        self.assertEqual(self.service.find_all(), [
            {
                'id': 1, 'name': 'Kalel'
            },
            {
                'id': 2, 'name': 'scaffold'
            },
        ])
