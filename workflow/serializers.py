from rest_framework import serializers
from .models import FormRequest, FormApproval

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormRequest
        fields = "__all__"


class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormApproval
        fields = "__all__"
