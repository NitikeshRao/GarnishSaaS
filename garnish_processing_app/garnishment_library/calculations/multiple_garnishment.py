import logging
from typing import Any, Dict, List, Optional
from garnish_processing_app.garnishment_library.helper import StateAbbreviations,MultipleGarnishmentPriorityHelper
from garnish_processing_app.garnishment_library.utility_class import CalculationResponse as CR
from .federal_case import FederalTax
from garnish_processing_app.garnishment_library.calculations import (StateTaxLevyCalculator, 
                                                        FederalTax, StudentLoanCalculator,ChildSupportHelper,CreditorDebtCalculator)
from constants.constants import (
    EmployeeFields as EE,
    CalculationFields as CF,
    PayrollTaxesFields as PT,
    GarnishmentTypeFields as GT,

)
import traceback as t 
from garnish_processing_app.models import PriorityOrders
from garnish_processing_app.serializers import PriorityOrderSerializer


logger = logging.getLogger(__name__)


# --- Custom Exceptions  ---
class GarnishmentError(Exception):
    """Base exception for garnishment calculation errors."""
    pass

class PriorityOrderError(GarnishmentError):
    """Error related to fetching or processing priority orders."""
    pass

class CalculationError(GarnishmentError):
    """Error occurring during a specific garnishment calculation."""
    pass

class InsufficientDataError(GarnishmentError):
    """Error for when required data is missing from the input record."""
    pass


class MultipleGarnishmentPriorityOrder:
    
    # --- Constants for Readability and Maintenance ---
    MAX_CALCULATED_GARNISHMENTS = 2
    CCPA_LIMIT_PERCENTAGE = 0.25
    
    _CALCULATOR_FACTORIES = {
        GT.CHILD_SUPPORT: lambda record: MultipleGarnishmentPriorityHelper().child_support_helper(record),
        GT.FEDERAL_TAX_LEVY: lambda record: FederalTax().calculate(record, config_data=None),
        GT.STUDENT_DEFAULT_LOAN: lambda record: StudentLoanCalculator().calculate(record),
        GT.STATE_TAX_LEVY: lambda record: StateTaxLevyCalculator().calculate(record, config_data=None),
        GT.CREDITOR_DEBT: lambda record: CreditorDebtCalculator().calculate(record, config_data=None),
    }

    def __init__(self, record: Dict[str, Any]):

        if not isinstance(record, dict):
            raise InsufficientDataError("Input 'record' must be a dictionary.")
            
        self.record = record
        self.work_state = self.record.get(EE.WORK_STATE)
        if not self.work_state:
            raise InsufficientDataError("Required field 'work_state' is missing from the record.")

        # Instantiate helpers that will be used across methods
        self.cs_helper = ChildSupportHelper(self.work_state)
        self.mg_helper = MultipleGarnishmentPriorityHelper()


    def _get_priority_order(self) -> List[Dict[str, Any]]:
        try:
            work_state_name = StateAbbreviations(self.work_state).get_state_name_and_abbr()
            if not work_state_name:
                raise ValueError("Could not resolve state name from abbreviation.")
            
            pri_order_qs = PriorityOrders.objects.select_related('state', 'garnishment_type').filter(
                state__state__iexact=work_state_name
            )
            
            if not pri_order_qs.exists():
                logger.warning(f"No priority order found for state: {self.work_state}")
                return []
                
            serializer = PriorityOrderSerializer(pri_order_qs, many=True)
            return serializer.data
        except Exception as e:
            # Catch specific ORM/serializer errors if possible, e.g., ValidationError
            logger.error(f"Failed to fetch priority order for state '{self.work_state}': {e}")
            raise PriorityOrderError(f"Database error fetching priority order for {self.work_state}.") from e

    def _get_calculator(self, garnishment_type: str) -> Optional[callable]:
        """
        Retrieves the calculation function for a given garnishment type.

        Args:
            garnishment_type: The type of garnishment (e.g., 'child_support').

        Returns:
            A callable function that will execute the calculation when called, 
            or None if not found.
        """
        factory = self._CALCULATOR_FACTORIES.get(garnishment_type.lower())
        
        if not factory:
            return None
        
        return lambda: factory(self.record)

    def _prepare_calculation_inputs(self) -> Dict[str, Any]:

        try:
            wages = self.record.get(CF.WAGES, 0)
            commission_and_bonus = self.record.get(CF.COMMISSION_AND_BONUS, 0)
            non_accountable_allowances = self.record.get(CF.NON_ACCOUNTABLE_ALLOWANCES, 0)
            payroll_taxes = self.record.get(PT.PAYROLL_TAXES)

            gross_pay = self.cs_helper.calculate_gross_pay(wages, commission_and_bonus, non_accountable_allowances)
            mandatory_deductions = self.cs_helper.calculate_md(payroll_taxes)
            disposable_earnings = self.cs_helper.calculate_de(gross_pay, mandatory_deductions)

            if disposable_earnings is None:
                raise InsufficientDataError("'disposable_earnings' could not be calculated.")

            return {
                "disposable_earnings": float(disposable_earnings),
                "garnishment_orders": self.record.get("garnishment_orders", []),
            }
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid financial data in record for state '{self.work_state}': {e}")
            raise InsufficientDataError("Invalid or missing financial data in record.") from e


    def calculate(self) -> Dict[str, Any]:

        try:
            inputs = self._prepare_calculation_inputs()
            disposable_earnings = inputs["disposable_earnings"]
            garnishment_orders = inputs["garnishment_orders"]
            
            if not garnishment_orders or not isinstance(garnishment_orders, list):
                logger.info("No garnishment orders found in record. Nothing to calculate.")
                return {"status": "No garnishment orders provided."}

            priority_list = self._get_priority_order()
        except GarnishmentError as e:
            logger.error(f"Halting calculation due to a setup error: {e}")
            return {"error": str(e)}

        available_for_garnishment = round(self.CCPA_LIMIT_PERCENTAGE * disposable_earnings, 2)
        garnishment_results = {}
        
        # --- Prepare the list of garnishments to process ---
        active_order_types = {g_type.strip().lower() for g_type in garnishment_orders}
        skip_types = {GT.FEDERAL_TAX_LEVY.lower(), GT.STATE_TAX_LEVY.lower()}
        
        applicable_orders = sorted(
            [
                item for item in priority_list
                if item.get('type', '').strip().lower() in active_order_types and
                   item.get('type', '').strip().lower() not in skip_types
            ],
            key=lambda x: x.get('priority_order', float('inf'))
        )

        calculated_count = 0
        
        # --- Main Calculation Loop ---
        for item in applicable_orders:
            g_type = item.get('type', '').strip().lower()
            if not g_type:
                continue

            if calculated_count >= self.MAX_CALCULATED_GARNISHMENTS or available_for_garnishment <= 0:
                # If we've hit our limit or have no money left, mark remaining as skipped
                garnishment_results[g_type] = {"withholding_amt": 0, "status": "skipped_due_to_limit_or_funds"}
                continue

            try:
                calculator_fn = self._get_calculator(g_type)
                if not calculator_fn:
                    logger.warning(f"No calculator found for type '{g_type}'.")
                    garnishment_results[g_type] = {"withholding_amt": 0, "status": "calculator_missing"}
                    continue
                
                # Execute the calculation
                result = calculator_fn()
                
                # --- Process the result based on garnishment type ---
                # This logic could be further encapsulated into a strategy pattern if it grows more complex
                amount_withheld = 0
                processed_result = {}

                if g_type == GT.CHILD_SUPPORT:
                    processed_result = self.mg_helper.distribute_child_support_amount(result, available_for_garnishment)
                    amount_withheld = sum(processed_result.get("result_amt", {}).values()) + sum(processed_result.get("arrear_amt", {}).values())
                elif g_type == GT.STUDENT_DEFAULT_LOAN:
                    processed_result = self.mg_helper.distribute_student_loan_amount(result, available_for_garnishment)
                    amount_withheld = sum(processed_result.get("student_loan_amt", {}).values())
                    processed_result["withholding_amt"] = amount_withheld # Normalize result structure
                elif g_type == GT.CREDITOR_DEBT:
                    base_amount = result.get("withholding_amt", 0)
                    amount_withheld = min(base_amount, available_for_garnishment) if base_amount > 0 else 0
                    result["withholding_amt"] = amount_withheld
                    processed_result = result
                else: # Generic handler for other types
                    base_amount = sum(result.values()) if isinstance(result, dict) else 0
                    amount_withheld = min(base_amount, available_for_garnishment) if base_amount > 0 else 0
                    processed_result = {"withholding_amt": amount_withheld}

                garnishment_results[g_type] = processed_result
                available_for_garnishment -= amount_withheld
                calculated_count += 1

            except Exception as e:
                logger.exception(f"Error calculating garnishment '{g_type}' for state '{self.work_state}'.")
                garnishment_results[g_type] = {"withholding_amt": 0, "status": "calculation_error", "error_details": str(e)}
                # We still increment count as this counts as a processed attempt
                calculated_count += 1
        
        return garnishment_results
    

# record=  {
#             "ee_id": "EE005131",
#             "work_state": "alabama"  ,
#             "no_of_exemption_including_self": 1,
#             "no_of_student_default_loan": 1,
#             "pay_period": "Biweekly",
#             "filing_status": "head_of_household",
#             "wages": 2800,

#             "commission_and_bonus": 205,
#             "non_accountable_allowances": 0,
#             "gross_pay": 2205,
#             "payroll_taxes": {
#                 "federal_income_tax": 250.0,
#                 "social_security_tax": 56.0,
#                 "medicare_tax": 13.5,
#                 "state_tax": 25.0,
#                 "local_tax": 0.0,
#                 "union_dues": 0,
#                 "wilmington_tax": 0,
#                 "medical_insurance_pretax": 0,
#                 "industrial_insurance": 0.0,
#                 "life_insurance": 0,
#                 "california_sdi": 0,
#                 "famli_tax": 0
#             },
#             "net_pay": 1860.5,
#             "is_blind": False,
#             "statement_of_exemption_received_date": "09-05-2024",
#             "garn_start_date": "09-05-2022",
#             "non_consumer_debt": True,
#             "consumer_debt": False,
#             "age": 64,
#             "spouse_age": 30,
#             "is_spouse_blind": True,
#             "support_second_family": "No",
#             "no_of_dependent_child": 1,
#             "arrears_greater_than_12_weeks": "No",
#             "garnishment_data": [
#                 {
#                     "type": "child support",
#                     "data": [
#                         {
#                             "case_id": "C17690",
#                             "ordered_amount": 210,
#                             "arrear_amount": 40
#                         },
#                         {
#                             "case_id": "C17690",
#                             "ordered_amount": 210,
#                             "arrear_amount": 40
#                         }
#                     ]
#                 }
#             ],
#         "garnishment_orders": [
#         "Child Support",
#         "creditor debt",
#         "federal tax levy"
#         ,"student default loan"]
#         }


# print("result_M",MultipleGarnishmentPriorityOrder(record).calculate())
