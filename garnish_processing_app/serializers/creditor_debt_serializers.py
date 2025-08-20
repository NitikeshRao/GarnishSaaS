from rest_framework import serializers
from garnish_processing_app.models.creditor_debt_models import (creditor_debt_applied_rule
                                        ,creditor_debt_exempt_amt_config,creditor_debt_rule,creditor_debt_rule_edit_permission)



class CreditorDebtAppliedRulesSerializers(serializers.ModelSerializer):
    class Meta:
        model = creditor_debt_applied_rule
        fields = '__all__'


class CreditorDebtExemptAmtConfigSerializers(serializers.ModelSerializer):
    class Meta:
        model = creditor_debt_exempt_amt_config
        fields = '__all__'

class CreditorDebtRuleSerializers(serializers.ModelSerializer):
    class Meta:
        model = creditor_debt_rule
        fields = '__all__'

class CreditorDebtRuleEditPermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = creditor_debt_rule_edit_permission
        fields = '__all__'
