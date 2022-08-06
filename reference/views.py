from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Reference, ReferenceRequest
from .permissions import (IsCandidateOrEvaluatorReadOnly,
                          IsEvaluatorOrCompanyAdminReadOnly)
from .serializers import ReferenceRequestSerializer, ReferenceSerializer


class ReferenceRequestView(APIView):
    permission_classes = [IsCandidateOrEvaluatorReadOnly]

    def post(self, request) -> Response:
        request_data = request.data.copy()
        request_data["requester"] = request.user.id

        request_serializer = ReferenceRequestSerializer(data=request_data)

        if request_serializer.is_valid():
            request_serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request) -> Response:
        evaluator = request.user

        reference_request = ReferenceRequest.objects.filter(
            writer_name=evaluator.username, writer_mobile=evaluator.mobile
        )
        if reference_request.exists():
            serializer = ReferenceRequestSerializer(reference_request, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)


class ReferenceView(APIView):
    permission_classes = [IsEvaluatorOrCompanyAdminReadOnly]

    def post(self, request) -> Response:
        try:
            request_data = request.data.copy()
            reference_request = request.data["request_id"]

            request_data["reference_request"] = reference_request
            request_data["writer"] = request.user.id

            reference_serializer = ReferenceSerializer(data=request_data)

            if reference_serializer.is_valid():
                reference_serializer.save()
                return Response(status=status.HTTP_200_OK)

            return Response(reference_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({"error": "INVALID_KEY"}, status=400)

    def get(self, request) -> Response:
        writer = request.query_params.get("writer")
        mobile = request.query_params.get("mobile")

        if not writer or not mobile:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        reference = Reference.objects.filter(writer__username=writer, writer__mobile=mobile)
        if reference.exists():
            serializer = ReferenceSerializer(reference, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)
