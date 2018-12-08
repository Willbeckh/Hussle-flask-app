import unittest
from app.forms.forms import LoginForm, RegisterForm, BusinessForm

class TestForm(unittest.TestCase):
    def setUp(self):
        self.login = LoginForm()
        self.register = RegisterForm()
        self.business = BusinessForm()
