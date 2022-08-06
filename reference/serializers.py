from rest_framework import serializers

from user.models import Company

from .models import ReferenceRequest as ReferenceRequestModel


class ReferenceRequestSerializer(serializers.ModelSerializer):
    requester_company = serializers.CharField()

    class Meta:
        model = ReferenceRequestModel
        fields = "__all__"

    def validate(self, data):
        try:
            data["requester_company"] = Company.objects.get(name=data["requester_company"])
            return data
        except Company.DoesNotExist:
            raise serializers.ValidationError("company not found.")
        except KeyError:
            raise serializers.ValidationError("requester_company key")
