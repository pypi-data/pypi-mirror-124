import os
from unittest.mock import MagicMock

from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from ihatemoney import models
from ihatemoney.currency_convertor import CurrencyConverter
from ihatemoney.run import create_app, db


class BaseTestCase(TestCase):

    SECRET_KEY = "TEST SESSION"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TESTING_SQLALCHEMY_DATABASE_URI", "sqlite://"
    )
    ENABLE_CAPTCHA = False

    def create_app(self):
        # Pass the test object as a configuration.
        return create_app(self)

    def setUp(self):
        db.create_all()
        # Add dummy data to CurrencyConverter for all tests (since it's a singleton)
        mock_data = {
            "USD": 1,
            "EUR": 0.8,
            "CAD": 1.2,
            "PLN": 4,
            CurrencyConverter.no_currency: 1,
        }
        converter = CurrencyConverter()
        converter.get_rates = MagicMock(return_value=mock_data)
        # Also add it to an attribute to make tests clearer
        self.converter = converter

    def tearDown(self):
        # clean after testing
        db.session.remove()
        db.drop_all()

    def login(self, project, password=None, test_client=None):
        password = password or project

        return self.client.post(
            "/authenticate",
            data=dict(id=project, password=password),
            follow_redirects=True,
        )

    def post_project(self, name, follow_redirects=True, default_currency="XXX"):
        """Create a fake project"""
        # create the project
        return self.client.post(
            "/create",
            data={
                "name": name,
                "id": name,
                "password": name,
                "contact_email": f"{name}@notmyidea.org",
                "default_currency": default_currency,
            },
            follow_redirects=follow_redirects,
        )

    def create_project(self, name, default_currency="XXX"):
        project = models.Project(
            id=name,
            name=str(name),
            password=generate_password_hash(name),
            contact_email=f"{name}@notmyidea.org",
            default_currency=default_currency,
        )
        models.db.session.add(project)
        models.db.session.commit()


class IhatemoneyTestCase(BaseTestCase):
    TESTING = True
    WTF_CSRF_ENABLED = False  # Simplifies the tests.

    def assertStatus(self, expected, resp, url=""):
        return self.assertEqual(
            expected,
            resp.status_code,
            f"{url} expected {expected}, got {resp.status_code}",
        )
