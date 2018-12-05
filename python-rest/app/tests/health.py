# -*- coding: utf-8 -*-

import unittest

from bootstrap.container import MockAppServicesInjector


class HealthTestCase(unittest.TestCase):
    def setUp(self):
        self.service = MockAppServicesInjector.health()

    def health_test_1_find_all(self):
        self.assertEqual(self.service.find_all(), [
            {
                'status': 'Ok'
            }
        ])
