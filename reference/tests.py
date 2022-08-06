import json

import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APIClient

from user.models import Company, User, UserType

from .models import ReferenceRequest


@pytest.mark.django_db
class TestReference:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.client = APIClient()
        self.user_type_candidate = self.create_user_type(name="candidate")
        self.user_type_evaluator = self.create_user_type(name="evaluator")
        self.company = self.create_company(name="company1")

        User.objects.create(
            email="candidate@test.com",
            password=make_password("12345678"),
            mobile="010-1111-1111",
            user_type=self.user_type_candidate,
        )
        User.objects.create(
            email="evaluator@test.com",
            password=make_password("12345678"),
            mobile="010-1111-1111",
            user_type=self.user_type_evaluator,
        )

    def create_user_type(self, **kwargs):
        user_type = UserType(**kwargs)
        user_type.save()
        return user_type

    def create_company(self, **kwargs):
        company = Company(**kwargs)
        company.save()
        return company

    def get_access_token(self, user_email):
        response_token = self.client.post(reverse("sign-in"), {"email": user_email, "password": "12345678"})
        return response_token.data["access"]

    def test_reference_request_auth(self) -> None:
        data = {"writer_type": "ceo"}
        response = self.client.post(reverse("refer-request"), data, fomrat="json")
        result = json.loads(response.content)

        assert response.status_code == 401
        assert result["detail"] == "서비스를 이용하기 위해 로그인 해주세요."

    def test_request_reference_with_evaluator(self) -> None:
        token = self.get_access_token("evaluator@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {"writer_type": "ceo"}
        response = self.client.post(reverse("refer-request"), data, fomrat="json")
        assert response.status_code == 403

    def test_request_reference_with_candidate(self) -> None:
        token = self.get_access_token("candidate@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "writer_type": "ceo",
            "writer_name": "lee",
            "writer_position": "manager",
            "writer_mobile": "010-2222-2222",
            "requester_company": "company1",
        }
        response = self.client.post(reverse("refer-request"), data, fomrat="json")

        assert response.status_code == 200

    def test_request_reference_with_wrong_company(self) -> None:
        token = self.get_access_token("candidate@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        data = {
            "writer_type": "ceo",
            "writer_name": "lee",
            "writer_position": "manager",
            "writer_mobile": "010-2222-2222",
            "requester_company": "company",
        }
        response = self.client.post(reverse("refer-request"), data, fomrat="json")
        response_body = json.loads(response.content)

        assert response.status_code == 400
        assert response_body["non_field_errors"] == ["company not found."]
