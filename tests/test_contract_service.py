import json
import os
import sqlite3
import tempfile
from unittest import TestCase
from unittest.mock import patch

from flask import Flask

from src.contractservice import create_app
from src.contractservice.db import get_db, init_db


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


class DBInitializationTest(TestCase):
    """Database initialization tests."""

    def setUp(self):
        app = create_app({
            'TESTING': True,
        })
        self.app = app

    @patch('src.contractservice.db.init_db')
    def test_init_db_command(self, fake_init_db):
        result = self.app.test_cli_runner().invoke(args=['init-db'])
        self.assertTrue(fake_init_db.called)
        self.assertIn('Initialized', result.output)


class ContractAPITest(TestCase):
    """Contract API tests."""

    def setUp(self):
        db_fd, db_path = tempfile.mkstemp()

        app = create_app({
            'TESTING': True,
            'DATABASE': db_path,
        })

        with app.app_context():
            init_db()

        self.app = app
        self.db_fd = db_fd
        self.db_path = db_path

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_get_contracts_with_no_items(self):
        expected_data = []

        response = self.app.test_client().get('/')
        received_data = json.loads(response.get_data(as_text=True).strip())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, received_data)

    def test_get_contracts_with_one_item(self):
        with self.app.app_context():
            cmd = 'INSERT INTO contract (id, debt, is_open) VALUES (1, 1.1, true)'
            get_db().executescript(cmd)
        expected_data = [{'id': 1, 'debt': 1.1, 'is_open': 1, 'closed_on': None}]

        response = self.app.test_client().get('/')
        received_data = json.loads(response.get_data(as_text=True).strip())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, received_data)

    def test_get_contracts_with_more_than_one_item(self):
        with self.app.app_context():
            cmd = ('INSERT INTO contract (id, debt, is_open, closed_on) '
                   'VALUES (1, 1.1, true, null), (2, 2.2, false, "2021-08-20")')
            get_db().executescript(cmd)
        expected_data = [
            {'id': 1, 'debt': 1.1, 'is_open': 1, 'closed_on': None},
            {'id': 2, 'debt': 2.2, 'is_open': 0, 'closed_on': '2021-08-20'},
        ]

        response = self.app.test_client().get('/')
        received_data = json.loads(response.get_data(as_text=True).strip())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, received_data)

    def test_get_contracts_filter_open(self):
        with self.app.app_context():
            cmd = ('INSERT INTO contract (id, debt, is_open, closed_on) '
                   'VALUES '
                   '(1, 1.1, true, null), (2, 2.2, false, "2021-08-20"),'
                   '(3, 3.3, true, null), (4, 4.4, false, "2021-08-14")')
            get_db().executescript(cmd)
        expected_data = [
            {'id': 1, 'debt': 1.1, 'is_open': 1, 'closed_on': None},
            {'id': 3, 'debt': 3.3, 'is_open': 1, 'closed_on': None},
        ]

        response = self.app.test_client().get('/?is_open=true')
        received_data = json.loads(response.get_data(as_text=True).strip())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, received_data)

    def test_get_contracts_filter_closed(self):
        with self.app.app_context():
            cmd = ('INSERT INTO contract (id, debt, is_open, closed_on) '
                   'VALUES '
                   '(1, 1.1, true, null), (2, 2.2, false, "2021-08-20"),'
                   '(3, 3.3, true, null), (4, 4.4, false, "2021-08-14")')
            get_db().executescript(cmd)
        expected_data = [
            {'id': 2, 'debt': 2.2, 'is_open': 0, 'closed_on': '2021-08-20'},
            {'id': 4, 'debt': 4.4, 'is_open': 0, 'closed_on': '2021-08-14'},
        ]

        response = self.app.test_client().get('/?is_open=false')
        received_data = json.loads(response.get_data(as_text=True).strip())

        self.assertEqual(200, response.status_code)
        self.assertEqual(expected_data, received_data)
