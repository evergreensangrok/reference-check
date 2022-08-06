import json

import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APIClient

from user.models import Company, User, UserType

from .models import Reference, ReferenceRequest


@pytest.mark.django_db
class TestReference:
    @pytest.fixture(autouse=True)
    def setup_class(self, db):
        self.client = APIClient()
        self.user_type_candidate = self.create_user_type(name="candidate")
        self.user_type_evaluator = self.create_user_type(name="evaluator")
        self.user_type_company_admin = self.create_user_type(name="company_admin")

        self.company = self.create_company(name="company1")

        self.candidate = User.objects.create(
            email="candidate@test.com",
            username="candidate",
            password=make_password("12345678"),
            mobile="010-1111-1111",
            user_type=self.user_type_candidate,
        )
        self.evaluator = User.objects.create(
            email="evaluator@test.com",
            username="ceo_name",
            password=make_password("12345678"),
            mobile="010-5678-5678",
            user_type=self.user_type_evaluator,
        )
        self.evaluator2 = User.objects.create(
            email="evaluator2@test.com",
            username="ceo_name2",
            password=make_password("12345678"),
            mobile="010-1234-1234",
            user_type=self.user_type_evaluator,
        )
        self.company_admin = User.objects.create(
            email="company_admin@test.com",
            username="company_admin",
            password=make_password("12345678"),
            mobile="010-1234-1234",
            user_type=self.user_type_company_admin,
        )

        self.create_reference_request_for_test()
        self.create_reference_for_test()

    def create_reference_request_for_test(self):
        self.reference_request = ReferenceRequest.objects.create(
            requester=self.candidate,
            writer_type="ceo",
            writer_name="ceo_name",
            writer_position="ceo",
            writer_mobile="010-5678-5678",
            requester_company=self.company,
        )

    def create_reference_for_test(self):
        Reference.objects.create(
            reference_request=self.reference_request,
            writer=self.evaluator,
            reference_comment="passionate and eager to learn",
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

    def test_get_reference_request_with_candidate(self) -> None:
        token = self.get_access_token("candidate@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(reverse("refer-request"))

        assert response.status_code == 403

    def test_get_reference_request_with_evaluator(self) -> None:
        token = self.get_access_token("evaluator@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(reverse("refer-request"))
        response_body = json.loads(response.content)

        assert response.status_code == 200
        assert response_body[0]["writer_name"] == "ceo_name"

    def test_request_reference_not_found_for_evaluator(self) -> None:
        token = self.get_access_token("evaluator2@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(reverse("refer-request"))
        assert response.status_code == 404

    def test_comment_reference_with_evaluator(self) -> None:
        token = self.get_access_token("evaluator@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {"request_id": 1, "reference_comment": "passionate and eager to learn"}
        response = self.client.post(reverse("refer-comment"), data, format="json")

        assert response.status_code == 200

    def test_comment_reference_with_candidate(self) -> None:
        token = self.get_access_token("candidate@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        data = {"request_id": 1, "reference_comment": "passionate and eager to learn"}
        response = self.client.post(reverse("refer-comment"), data, format="json")

        assert response.status_code == 403

    def test_get_reference_with_candidate(self) -> None:
        token = self.get_access_token("candidate@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(reverse("refer-comment"))

        assert response.status_code == 403

    def test_get_reference_request_with_company_admin(self) -> None:
        token = self.get_access_token("company_admin@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        parameters = {"mobile": "010-5555-6666"}
        response = self.client.get(
            reverse("refer-comment") + "?mobile=010-5678-5678&writer=ceo_name", params=parameters
        )
        response_body = json.loads(response.content)

        assert response.status_code == 200
        assert response_body[0]["reference_comment"] == "passionate and eager to learn"

    def test_get_reference_request_without_writer(self) -> None:
        token = self.get_access_token("company_admin@test.com")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("refer-comment") + "?mobile=010-5678-5678")
        assert response.status_code == 400
