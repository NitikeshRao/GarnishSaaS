from rest_framework import serializers
from employee.models import employee_detail

class EmployeeDetailsSerializer(serializers.ModelSerializer):

    is_blind = serializers.BooleanField(required=False, allow_null=True)
    support_second_family = serializers.BooleanField(
        required=False, allow_null=True)
    spouse_age = serializers.IntegerField(required=False, allow_null=True)
    is_spouse_blind = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = employee_detail
        fields = '__all__'

