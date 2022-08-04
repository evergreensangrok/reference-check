from rest_framework.test import APIClient


def test_ping():
    response = APIClient().get("/ping")
    assert response.data == {"pong"}
