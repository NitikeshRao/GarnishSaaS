from rest_framework import serializers
from garnish_processing_app.models.garnishment_fees_models import (garnishment_fees,garnishment_fees_states_rule,
                                                    garnishment_fees_rules)

class GarnishmentFeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = garnishment_fees
        fields = '__all__'


class GarnishmentFeesStatesRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = garnishment_fees_states_rule
        fields = ['id', 'state', 'pay_period', 'rule']


class GarnishmentFeesRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = garnishment_fees_rules
        fields = ['id', 'rule', 'maximum_fee_deduction',
                  'per_pay_period', 'per_month', 'per_remittance']