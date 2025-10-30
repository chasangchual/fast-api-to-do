import uuid

import pytest

from app.models import User

@pytest.fixture
def new_user():
    new_user:User = User()
    new_user.public_id = uuid.uuid4()
    new_user.email = 'test@user.com'
    new_user.password = 'zbv9dRfk$%d'
    new_user.first_name = 'test'
    new_user.last_name = 'user'
    new_user.role = 'USER'
    new_user.is_active = True
    new_user.

    return User(username='moringa',password='<PASSWORD>')

def test_check_instance_variables(self):
    self.assertEquals(self.new_user.username,'moringa')
    self.assertEquals(self.new_user.password,'<PASSWORD>')