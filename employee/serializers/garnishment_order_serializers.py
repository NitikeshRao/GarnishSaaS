from rest_framework import serializers
from employee.models import garnishment_order,withholding_order_data

class WithholdingOrderDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = withholding_order_data
        fields = '__all__'

class GarnishmentOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = garnishment_order
        fields = '__all__'