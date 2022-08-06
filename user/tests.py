import os

import dotenv
import pytest

dotenv.read_dotenv()

from .models import User


@pytest.mark.django_db
def test_user_create():
    User.objects.create(email="candidate@test.com", password=os.environ.get("CI_TEST_PASS"))
    assert User.objects.count() == 1
