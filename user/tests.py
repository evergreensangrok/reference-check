import json
import os

import dotenv
import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APIClient

dotenv.read_dotenv()

from .models import CareerInterest, Company, User, UserType


@pytest.mark.django_db
def test_user_create():
    User.objects.create(email="candidate@test.com", password=os.environ.get("CI_TEST_PASS"))
    assert User.objects.count() == 1


@pytest.mark.django_db
class TestUser:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.test_pass = os.environ.get("CI_TEST_PASS")
        self.client = APIClient()

        self.user_type_candidate = self.create_user_type(name="candidate")
        self.user_type_evaluator = self.create_user_type(name="evaluator")
        self.company = self.create_company(name="company1")
        self.career_interest = self.create_career_interest(career="it")
        User.objects.create(
            email="candidate@test.com", password=make_password(os.environ.get("CI_TEST_PASS")), mobile="010-1111-1111"
        )

    def create_user_type(self, **kwargs):
        user_type = UserType(**kwargs)
        user_type.save()
        return user_type

    def create_company(self, **kwargs):
        company = Company(**kwargs)
        company.save()
        return company

    def create_career_interest(self, **kwargs):
        career_interest = CareerInterest(**kwargs)
        career_interest.save()
        return career_interest

    def test_user_registration(self) -> None:
        data = {
            "email": "candidate2@test.com",
            "password": self.test_pass,
            "user_type": 1,
            "career_interest": 1,
            "mobile": "010-1111-1111",
        }
        response = self.client.post(reverse("sign-up"), data, fomrat="json")
        assert response.status_code == 200

    def test_user_registration_with_duplicate_email(self) -> None:
        data = {"email": "candidate@test.com", "password": self.test_pass, "user_type": 1, "career_interest": 1}
        response = self.client.post(reverse("sign-up"), data, fomrat="json")
        response_body = json.loads(response.content)

        assert response.status_code == 400
        assert response_body["email"] == ["user with this email already exists."]

    def test_user_registration_with_user_type_pk_input(self) -> None:
        data = {
            "email": "candidate3@test.com",
            "password": self.test_pass,
            "user_type": "candidate",
            "career_interest": 1,
        }
        response = self.client.post(reverse("sign-up"), data, fomrat="json")
        response_body = json.loads(response.content)

        assert response.status_code == 400
        assert response_body["user_type"] == ["Incorrect type. Expected pk value, received str."]

    def test_user_sign_in(self) -> None:
        data = {"email": "candidate@test.com", "password": self.test_pass}
        response = self.client.post(reverse("sign-in"), data, fomrat="json")
        assert response.status_code == 200
