from django.db import models

from user.models import Company, Department, User


class ReferenceRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    writer_type = models.CharField(max_length=128)  # ceo, colleague
    writer_name = models.CharField(max_length=128)
    writer_position = models.CharField(max_length=128)
    writer_mobile = models.CharField(max_length=128)
    requester_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reference_requests"

    def __str__(self):
        return f"{self.requester} - request"
