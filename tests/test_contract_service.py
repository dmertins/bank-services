import sqlite3
from unittest import TestCase

from flask import Flask

from src.contractservice import create_app
from src.contractservice.db import get_db


class AppFactoryTest(TestCase):
    """Application factory function tests."""
    
    def test_app_instance_creation(self):
        self.assertIsInstance(create_app(), Flask)

    def test_app_config(self):
        self.assertFalse(create_app().testing)
        self.assertTrue(create_app({'TESTING': True}).testing)


class DBConnectionTest(TestCase):
    """Database connection tests."""

    def setUp(self):
        app = create_app({
            'TESTING': True,
        })
        self.app = app

    def test_connection_reuse_in_same_request_context(self):
        with self.app.app_context():
            db = get_db()
            self.assertIs(db, get_db())

    def test_connection_is_closed_outside_request_context(self):
        with self.app.app_context():
            db = get_db()

        with self.assertRaises(sqlite3.ProgrammingError) as cm:
            db.executescript('SELECT 1')

        self.assertIn('closed database', str(cm.exception))
