from rest_framework import serializers

from user.models import Company

from .models import Reference as ReferenceModel
from .models import ReferenceRequest as ReferenceRequestModel


class ReferenceRequestSerializer(serializers.ModelSerializer):
    requester_company = serializers.CharField()
    requester_info = serializers.SerializerMethodField()

    class Meta:
        model = ReferenceRequestModel
        fields = [
            "id",
            "requester",
            "requester_company",
            "writer_type",
            "writer_name",
            "writer_position",
            "writer_mobile",
            "requester_info",
        ]

    def get_requester_info(self, obj):
        return obj.requester.email

    def validate(self, data):
        try:
            data["requester_company"] = Company.objects.get(name=data["requester_company"])
            return data
        except Company.DoesNotExist:
            raise serializers.ValidationError("company not found.")
        except KeyError:
            raise serializers.ValidationError("requester_company key")


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceModel
        fields = "__all__"
