from rest_framework import serializers

from garnish_processing_app.models.state_tax_models import (state_tax_levy_applied_rule,state_tax_levy_config
                                              ,state_tax_levy_exempt_amt_config,state_tax_levy_rule_edit_permission)


class StateTaxLevyConfigSerializers(serializers.ModelSerializer):
    class Meta:
        model = state_tax_levy_config
        fields = '__all__'

class StateTaxLevyRulesSerializers(serializers.ModelSerializer):
    class Meta:
        model = state_tax_levy_applied_rule
        exclude = ['id']


class StateTaxLevyExemptAmtConfigSerializers(serializers.ModelSerializer):
    class Meta:
        model = state_tax_levy_exempt_amt_config
        fields = '__all__'


class StateTaxLevyRuleEditPermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = state_tax_levy_rule_edit_permission
        fields = '__all__'