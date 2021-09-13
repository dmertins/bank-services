from unittest import TestCase

from flask import Flask

from src.contractservice import create_app


class AppFactoryTest(TestCase):
    """Application factory function tests."""
    
    def test_app_instance_creation(self):
        self.assertIsInstance(create_app(), Flask)

    def test_app_config(self):
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({'TESTING': True}).testing)
