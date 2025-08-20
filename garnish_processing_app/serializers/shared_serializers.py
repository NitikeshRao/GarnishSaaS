from rest_framework import serializers
from garnish_processing_app.models.shared_models import (
    PayPeriod, State, ExemptConfig, PriorityOrders,ThresholdAmount,GarnishmentType)

class PayPeriodSerializers(serializers.ModelSerializer):

    class Meta:
        model = PayPeriod
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):

    class Meta :
        model = State
        fields = '__all__'

class GarnishmentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GarnishmentType
        fields = '__all__'

class ExemptConfigSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='state.state', read_only=True)         
    pay_period = serializers.CharField(source='pay_period.name', read_only=True) 

    class Meta:
        model = ExemptConfig
        fields = [
            'debt_type', 'is_filing_status', 'wage_basis',
            'wage_amount', 'percent_limit', 'state', 'pay_period'
        ]
class ThresholdAmountSerializer(serializers.ModelSerializer):
    debt_type = serializers.CharField(source='config.debt_type', read_only=True)
    is_filing_status = serializers.BooleanField(source='config.is_filing_status', read_only=True)
    wage_amount = serializers.FloatField(source='config.wage_amount', read_only=True)
    percent_limit = serializers.IntegerField(source='config.percent_limit', allow_null=True, read_only=True)
    state = serializers.CharField(source='config.state.state', read_only=True)
    pay_period = serializers.CharField(source='config.pay_period.name', read_only=True)
    start_gt_5dec24= serializers.BooleanField(source='config.start_gt_5dec24', read_only=True)

    class Meta:
        model = ThresholdAmount
        fields = [
            'id',
            'debt_type', 'is_filing_status', 'wage_amount', 'percent_limit',
            'state', 'pay_period', 'lower_threshold_amount', 'lower_threshold_percent1', 'lower_threshold_percent2',
            'mid_threshold_amount', 'mid_threshold_percent',
            'upper_threshold_amount', 'upper_threshold_percent',
            'de_range_lower_to_upper_threshold_percent',
            'de_range_lower_to_mid_threshold_percent',
            'de_range_mid_to_upper_threshold_percent',
            'filing_status_percent','start_gt_5dec24','exempt_amt'
        ]

class PriorityOrderSerializer(serializers.ModelSerializer):
    state = serializers.CharField(source='state.state', read_only=True)         
    type = serializers.CharField(source='garnishment_type.type', read_only=True) 

    class Meta:
        model = PriorityOrders
        fields = [
            'priority_order',  'type', 'state'
        ]