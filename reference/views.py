from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsCandidateOrEvaluatorReadOnly
from .serializers import ReferenceRequestSerializer


class ReferenceRequestView(APIView):
    permission_classes = [IsCandidateOrEvaluatorReadOnly]

    def post(self, request) -> Response:
        # print(request.user)
        # request.data['requester'] = request.user.id
        request_data = request.data.copy()
        request_data["requester"] = request.user.id
        request_serializer = ReferenceRequestSerializer(data=request_data)

        if request_serializer.is_valid():
            request_serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
