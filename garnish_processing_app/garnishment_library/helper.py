import json
import os
from django.core.exceptions import ObjectDoesNotExist
from garnish_processing_app.models import WithholdingRules, WithholdingLimit,State

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from constants.constants import (
    AllocationMethods as AM,
    EmployeeFields as EE,
    CalculationFields as CF,
    PayrollTaxesFields as PT,
    CalculationMessages as CM,
    GarnishmentTypeFields as GT,
    ExemptConfigFields as EC,
    CommonConstants as CC,
    PayPeriodFields as PP
)
import traceback as t


FMW_RATE = 7.25
PAY_PERIOD_MULTIPLIER = {
    PP.WEEKLY: 30,
    PP.BI_WEEKLY: 60,
    PP.SEMI_MONTHLY: 65,
    PP.MONTHLY: 130,
}

class Helper:

    def get_support_amounts_by_type(self, garnishment_data, amount_type):
        """
        Retrieves a list of amounts from the record based on the provided amount_type.

        :param record: The data record containing garnishment information.
        :param amount_type: The prefix key to filter amounts (e.g., 'ordered_amount' or 'arrear_amount').
        :return: List of filtered amount values.
        """
        try:
            return [
                val for item in garnishment_data[0]["data"]
                for key, val in item.items()
                if key.lower().startswith(amount_type.lower())
            ]
        except Exception as e:
            raise ValueError(f"Error extracting amounts for type '{amount_type}': {str(e)}")
        

    def calculate_each_amount(self, amounts, label):
        """
        Returns a dictionary of each amount keyed by order and type (e.g., child support or arrears).
        
        Args:
            amounts (list): List of amounts
            label (str): Type of amount ('child support amount' or 'arrear amount')

        Returns:
            dict: Dictionary with keys like 'child support amount1', 'arrear amount1', etc.
        """
        try:
            return {
                f"{label}{i+1}": amt
                for i, amt in enumerate(amounts)
            }
        except Exception as e:
            raise ValueError(
                f"Error calculating each {label}: {str(e)}"
            )



class ExemptAmount:

    def get_fmw(self, pay_period):
        """
        Returns the Federal Minimum Wage threshold for the given pay period.
        """
        if not pay_period:
            raise ValueError("Pay period is missing in the record.")
        multiplier = PAY_PERIOD_MULTIPLIER.get(pay_period.lower())
        if not multiplier:
            raise ValueError(f"Invalid pay period: {pay_period}")
        return FMW_RATE * multiplier
    
class AllocationMethodResolver:
    
    """
    Identifies the allocation method for a given work state using the database.
    """

    def __init__(self, work_state):
        # Normalize and lower the state name or abbreviation
        self.work_state = StateAbbreviations(work_state).get_state_name_and_abbr().lower()

    def get_allocation_method(self):
        """
        Fetches the allocation method from the WithholdingRules table based on the work state.
        """
        try:
            rule = WithholdingRules.objects.get(state__state__iexact=self.work_state)
            if rule.allocation_method:
                return rule.allocation_method.lower()
            return f"No allocation method defined for the state: {self.work_state.capitalize()}."
        
        except ObjectDoesNotExist:
            return f"No withholding rule found for the state: {self.work_state.capitalize()}."
        
        except MultipleObjectsReturned:
            return f"Multiple withholding rules found for the state: {self.work_state.capitalize()}. Please verify data integrity."
        
        except Exception as e:
            return f"Unexpected error while fetching allocation method: {str(e)}"
        

class WLIdentifier:
    """
    Identifies withholding limits for a given state and employee using database models.
    """

    def get_state_rule(self, work_state):
        """
        Returns the WithholdingRules object for the given state abbreviation.
        """
        try:
            work_state_name = StateAbbreviations(work_state).get_state_name_and_abbr()
            rule_obj = WithholdingRules.objects.filter(
                state__state__iexact=work_state_name
            ).first()

            if not rule_obj:
                raise ValueError(f"No rule found for the state: {work_state_name}")

            return rule_obj

        except Exception as e:
            raise RuntimeError(f"Error retrieving rule for state '{work_state}': {e}")

    def find_wl_value(self, work_state, employee_id, supports_2nd_family, arrears_of_more_than_12_weeks, de_gt_145, order_gt_one):
        """
        Finds the withholding limit (WL) value based on state rule and employee attributes.
        """
        try:
            rule_obj = self.get_state_rule(work_state)

            filters = {
                "rule": int(rule_obj.rule),
                "supports_2nd_family": supports_2nd_family,
                "arrears_of_more_than_12_weeks": arrears_of_more_than_12_weeks,
            }
            filters["number_of_orders"]=None
            filters["weekly_de_code"] = None
            
            if order_gt_one:
                filters["number_of_orders"] = order_gt_one
            if de_gt_145:
                filters["weekly_de_code"] = de_gt_145

            limit = WithholdingLimit.objects.filter(**filters).first()
            
            if not limit:
                raise ValueError(f"No matching WL found for employee {employee_id}")
            return int(limit.wl) / 100

        except Exception as e:
            raise RuntimeError(f"Error finding WL value: {e}")



def change_record_case(record):
    """
    Converts all keys in the record to snake_case and lower case.
    """
    try:
        new_record = {}
        for key, value in record.items():
            new_key = key.replace(' ', '_').lower()
            new_record[new_key] = value
        return new_record
    except Exception as e:
        raise ValueError(f"Error changing record case: {e}")


class StateAbbreviations:
    """
    Utility for converting state abbreviations to full state names.
    """

    def __init__(self, abbreviation):
        self.abbreviation = abbreviation.lower()

    def get_state_name_and_abbr(self):
        """
        Returns the full state name for a given abbreviation, or the input if not found.
        """
        state_abbreviations = {
            "al": "alabama", "ak": "alaska", "az": "arizona", "ar": "arkansas",
            "ca": "california", "co": "colorado", "ct": "connecticut", "de": "delaware",
            "fl": "florida", "ga": "georgia", "hi": "hawaii", "id": "idaho",
            "il": "illinois", "in": "indiana", "ia": "iowa", "ks": "kansas",
            "ky": "kentucky", "la": "louisiana", "me": "maine", "md": "maryland",
            "ma": "massachusetts", "mi": "michigan", "mn": "minnesota", "ms": "mississippi",
            "mo": "missouri", "mt": "montana", "ne": "nebraska", "nv": "nevada",
            "nh": "new hampshire", "nj": "new jersey", "nm": "new mexico", "ny": "new york",
            "nc": "north carolina", "nd": "north dakota", "oh": "ohio", "ok": "oklahoma",
            "or": "oregon", "pa": "pennsylvania", "ri": "rhode island", "sc": "south carolina",
            "sd": "south dakota", "tn": "tennessee", "tx": "texas", "ut": "utah",
            "vt": "vermont", "va": "virginia", "wa": "washington", "wv": "west virginia",
            "wi": "wisconsin", "wy": "wyoming"
        }
        if len(self.abbreviation) != 2:
            state_name = self.abbreviation
        else:
            state_name = state_abbreviations.get(
                self.abbreviation, self.abbreviation)
        return state_name
    

class MultipleGarnishmentPriorityHelper:
    """
    Class to determine the priority order of multiple garnishments based on state rules.
    """

    def distribute_child_support_amount(self,result, available_amount):
        result_amt = result.get("result_amt", {})
        arrear_amt = result.get("arrear_amt", {})

        final_result_amt = {}
        final_arrear_amt = {}

        # Process result_amt first
        for key, value in result_amt.items():
            if available_amount >= value:
                final_result_amt[key] = value
                available_amount -= value
            elif available_amount > 0:
                final_result_amt[key] = available_amount
                available_amount = 0
            else:
                final_result_amt[key] = 0

        # Then process arrear_amt
        for key, value in arrear_amt.items():
            if available_amount >= value:
                final_arrear_amt[key] = value
                available_amount -= value
            elif available_amount > 0:
                final_arrear_amt[key] = available_amount
                available_amount = 0
            else:
                final_arrear_amt[key] = 0

        return {
            "result_amt": final_result_amt,
            "arrear_amt": final_arrear_amt
        }

        
    def distribute_student_loan_amount(self, result, available_amount):
        """
        Distributes the student loan amount based on the available amount.
        Gives full amounts if possible, otherwise partial, and stops when funds run out.
        """
        student_loan_amt = result.get("student_loan_amt", {})
        final_student_loan_amt = {}

        for key, value in student_loan_amt.items():
            if available_amount >= value:
                final_student_loan_amt[key] = value
                available_amount -= value
            elif available_amount > 0:
                final_student_loan_amt[key] = available_amount
                available_amount = 0
            else:
                final_student_loan_amt[key] = 0

        return {"student_loan_amt": final_student_loan_amt}
    
    def child_support_helper(self,record):

        from garnish_processing_app.garnishment_library import ChildSupportHelper
        """
        Returns an instance of ChildSupportHelper for the given state.
        """
        try:
            #
            state_name=record.get(EE.WORK_STATE)
            wages = record.get(CF.WAGES, 0)
            commission_and_bonus = record.get(CF.COMMISSION_AND_BONUS, 0)
            pay_period = record.get(EE.PAY_PERIOD.lower())
            non_accountable_allowances = record.get(CF.NON_ACCOUNTABLE_ALLOWANCES, 0)
            payroll_taxes = record.get(PT.PAYROLL_TAXES)
            employee_id = record.get(EE.EMPLOYEE_ID)
            supports_2nd_family = record.get(EE.SUPPORT_SECOND_FAMILY)
            arrears_12ws = record.get(EE.ARREARS_GREATER_THAN_12_WEEKS)
            garnishment_data = record.get('garnishment_data', [])
            

            #
            cs_helper=ChildSupportHelper(state_name)
            exempt_amount = ExemptAmount().get_fmw(pay_period)
            gross_pay = cs_helper.calculate_gross_pay(wages, commission_and_bonus, non_accountable_allowances)
            mandatory_deductions=cs_helper.calculate_md(payroll_taxes)
            garnishment_data = record.get('garnishment_data')
            disposable_earnings=cs_helper.calculate_de(gross_pay,mandatory_deductions)
            withholding_limit =cs_helper.calculate_wl(employee_id, supports_2nd_family, arrears_12ws, disposable_earnings, garnishment_data)
            ade=cs_helper.calculate_ade(withholding_limit, disposable_earnings)
            diff_of_de_and_exempt_amount =disposable_earnings-exempt_amount 
            support_amount = Helper().get_support_amounts_by_type(garnishment_data,CF.ORDERED_AMOUNT )
            arrear_amount = Helper().get_support_amounts_by_type(garnishment_data,CF.ARREAR_AMOUNT )
            total_child_support_amount = sum(support_amount)
            total_arrear_amount = sum(arrear_amount)
            sum_of_order_amount = total_child_support_amount+total_arrear_amount
            total_withholding_amount =min(sum_of_order_amount,diff_of_de_and_exempt_amount,ade)
            withholding_amount = cs_helper.calculate_twa(support_amount, arrear_amount)
            alloc_method = AllocationMethodResolver(state_name).get_allocation_method()


            if ade >= total_withholding_amount:
                cs_amounts = Helper().calculate_each_amount(support_amount,"child support amount") 
                ar_amounts = Helper().calculate_each_amount(arrear_amount,"arrear amount") 
            else:
                cs_amounts, ar_amounts = {}, {}
                if alloc_method == AM.PRORATE:
                    # Prorate support amounts
                    cs_amounts = {
                        f"child support amount{i+1}": round((amt / total_withholding_amount) * ade, 2) if gross_pay > 0 else 0
                        for i, amt in enumerate(total_child_support_amount)
                    }
                    arrear_pool = withholding_amount - sum(total_child_support_amount)
                    total_arrears = sum(total_arrear_amount)
                    # Prorate arrear amounts
                    ar_amounts = {
                        f"arrear amount{i+1}": (
                            round((amt / total_arrears) * arrear_pool, 2)
                            if total_arrears and arrear_pool > 0 and gross_pay > 0 else 0
                        ) for i, amt in enumerate(total_arrear_amount)
                    }
                elif alloc_method == AM.DEVIDEEQUALLY:
                    # Divide equally among orders
                    split_amt = round(ade / len(total_child_support_amount), 2) if total_child_support_amount else 0
                    cs_amounts = {
                        f"child support amount{i+1}": split_amt if gross_pay > 0 else 0
                        for i in range(len(total_child_support_amount))
                    }
                    arrear_pool = ade - sum(total_child_support_amount)
                    ar_amounts = {
                        f"arrear amount{i+1}": round(amt / len(total_arrear_amount), 2) if arrear_pool > 0 and gross_pay > 0 else 0
                        for i, amt in enumerate(total_arrear_amount)
                    }
                else:
                    raise ValueError(
                        "Invalid allocation method for garnishment.")

            return {
                "result_amt": cs_amounts,
                "arrear_amt": ar_amounts,
                "ade": ade,
                "de": disposable_earnings,
                "mde": mandatory_deductions
            }
        
        except Exception as e:
            raise RuntimeError(f"Error initializing ChildSupportHelper for state '{state_name}': {e}")

