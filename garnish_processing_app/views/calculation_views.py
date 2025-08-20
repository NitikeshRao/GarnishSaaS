from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import traceback as t
from garnish_processing_app.services.calculation_service import CalculationDataView
from garnish_processing_app.garnishment_library.utility_class import ResponseHelper
from employee.constants import (
    EmployeeFields as EE,
    BatchDetail
)
from garnish_processing_app.garnishment_library.calculations.multiple_garnishment import MultipleGarnishmentPriorityOrder
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer



class PostCalculationView(APIView):
    """Handles Garnishment Calculation API Requests"""

    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def get_all_garnishment_types(self, cases_data):
        """Extract all unique garnishment types from the cases data."""
        return {
            garnishment.get(EE.GARNISHMENT_TYPE).lower().strip()
            for case in cases_data
            for garnishment in case.get(EE.GARNISHMENT_DATA, [])
            if garnishment.get(EE.GARNISHMENT_TYPE).lower().strip()
        }

    def post(self, request, *args, **kwargs):
        batch_id = request.data.get(BatchDetail.BATCH_ID)
        cases_data = request.data.get("cases", [])

        if not batch_id:
            return self._respond({"error": "batch_id is required"}, status.HTTP_400_BAD_REQUEST)

        if not cases_data:
            return self._respond({"error": "No rows provided"}, status.HTTP_400_BAD_REQUEST)

        output = []
        calculation_service = CalculationDataView()

        garnishment_types = self.get_all_garnishment_types(cases_data)
        config_data = calculation_service.preload_config_data(garnishment_types)

        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_case = {
                executor.submit(calculation_service.process_and_store_case, case_info, batch_id, config_data): case_info
                for case_info in cases_data
            }

            for future in as_completed(future_to_case):
                case_info_original = future_to_case[future]
                ee_id_for_log = case_info_original.get(EE.EMPLOYEE_ID, "N/A")
                try:
                    result = future.result()
                    if result:
                        output.append(result)
                except Exception as e:
                    error_message = f"Error processing garnishment for employee {ee_id_for_log}: {e}"
                    output.append({
                        "error": error_message,
                        "status": status.HTTP_500_INTERNAL_SERVER_ERROR
                    })

        if all("error" in item for item in output) and output:
            return self._respond({
                'message': 'Errors occurred during processing of some cases.',
                'results': output,
                'success': False,
                'batch_id': batch_id
            }, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return self._respond({
            "success": True,
            "message": "Result Generated Successfully",
            "status_code": status.HTTP_200_OK,
            "batch_id": batch_id,
            "results": output
        }, status.HTTP_200_OK)

    def _respond(self, data, status_code):
        """
        Helper method to return either JSON or render an HTML page,
        depending on the requested format.
        """
        if self.request.accepted_renderer.format == 'html':
            # Renders the HTML template with the same data
            return Response(data, template_name='calculation_result.html', status=status_code)
        return Response(data, status=status_code)
