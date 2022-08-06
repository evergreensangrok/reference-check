import os

import dotenv
import pytest

dotenv.read_dotenv()

from .models import User


@pytest.mark.django_db
def test_user_create():
    User.objects.create(email="candidate@test.com", password=os.environ.get("TEST_USER_PASSWORD"))
    assert User.objects.count() == 1
