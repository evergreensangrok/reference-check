from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code = status_code
        super().__init__(detail=detail, code=code)


class IsCandidateOrEvaluatorReadOnly(BasePermission):
    """
    지원자는 POST 가능, 평가자는 조회만 가능
    """

    message = "접근 권한이 없습니다."

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            response = {
                "detail": "서비스를 이용하기 위해 로그인 해주세요.",
            }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if user.user_type.name == "candidate" and request.method == "POST":
            return True

        if user.user_type.name == "evaluator" and request.method == "GET":
            return True

        return False
