from rest_framework import status
from rest_framework.response import Response
from constants.constants import  EmployeeFields
from .child_support import ChildSupportHelper
from garnish_processing_app.garnishment_library.helper import StateAbbreviations,ExemptAmount


class StudentLoan:
    """
    Handles calculation of Student Loan garnishment amounts based on federal and state rules.
    """

    def _calculate_disposable_earnings(self, record):
        """
        Calculates disposable earnings by subtracting mandatory deductions from gross pay.
        """
        state = StateAbbreviations(record.get(
            EmployeeFields.WORK_STATE)).get_state_name_and_abbr()
        de = ChildSupportHelper(state).calculate_de(record)
        return de

    def get_single_student_amount(self, record):
        """
        Calculates the garnishment amount for a single student loan.
        """
        try:
            de = self._calculate_disposable_earnings(record)
            fmw = ExemptAmount.get_fmw(record.get(EmployeeFields.PAY_PERIOD))

            if de <= fmw:
                return {
                    "student_loan_amt": "Student loan withholding cannot be applied because Disposable Earnings are less than or equal to the exempt amount."
                }

            deduction = min(de * 0.15, de * 0.25, de - fmw)
            return {"student_loan_amt": {"student_loan_amt1": round(deduction, 2)}, "disposable_earning": de}

        except Exception as e:
            return {
                "student_loan_amt": {"student_loan_amt1": f"Error calculating single student loan amount: {e}"}
            }

    def get_multiple_student_amount(self, record):
        """
        Calculates the garnishment amounts for multiple student loans.
        """
        try:
            de = self._calculate_disposable_earnings(record)
            fmw = ExemptAmount.get_fmw(record.get(EmployeeFields.PAY_PERIOD))
      
            if de <= fmw:
                msg = "Student loan withholding cannot be applied because Disposable Earnings are less than or equal to the exempt amount."
                return {"student_loan_amt": {"student_loan_amt1": msg, "student_loan_amt2": msg}, "disposable_earning": de}

            return {"student_loan_amt": {"student_loan_amt1": round(de * 0.15, 2),
                                         "student_loan_amt2": round(de * 0.10, 2)}, "disposable_earning": de}

        except Exception as e:
            return {"student_loan_amt": {
                "student_loan_amt1": f"Error calculating multiple student loan amount: {e}",
                "student_loan_amt2": f"Error calculating multiple student loan amount: {e}"
            }, "disposable_earning": de}


class StudentLoanCalculator:
    """
    Service to calculate student loan garnishment for single or multiple cases.
    """

    def calculate(self, record):
        """
        Determines and calculates the appropriate student loan garnishment amount(s).
        Returns a DRF Response object on error.
        """
        try:
            count = record.get(EmployeeFields.NO_OF_STUDENT_DEFAULT_LOAN)
            student_loan = StudentLoan()

            if count == 1:
                return student_loan.get_single_student_amount(record)
            elif count and count > 1:
                return student_loan.get_multiple_student_amount(record)
            else:
                return {"student_loan_amt": {"student_loan_amt1": 0, "de": 0}}

        except Exception as e:
            return Response(
                {
                    "error": str(e),
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
