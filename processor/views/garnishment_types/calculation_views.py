from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import traceback as t
from processor.services.calculation_service import CalculationDataView
from processor.garnishment_library.utils.response import ResponseHelper
from user_app.constants import (
    EmployeeFields as EE,
    BatchDetail
)
from processor.garnishment_library.calculations.multiple_garnishment import MultipleGarnishmentPriorityOrder
from datetime import datetime


import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from typing import Dict, Set, List, Any

logger = logging.getLogger(__name__)

from rest_framework.views import APIView
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class PostCalculationView(APIView):
    """Handles Garnishment Calculation API Requests with Multi-Type Support"""
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    
    template_name = 'garnish-process-app/batch-process/index.html'

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                BatchDetail.BATCH_ID: openapi.Schema(type=openapi.TYPE_STRING, description="Batch ID"),
                "cases": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT))
            },
            required=[BatchDetail.BATCH_ID, "cases"]
        ),
        responses={
            200: 'Batch processed successfully',
            400: 'Invalid input (missing batch_id or cases)',
            500: 'Internal server error'
        }
    )
    def get(self, request):
        """Render empty page (useful for HTML mode)."""
        return Response({}, template_name=self.template_name)

    def post(self, request, *args, **kwargs):
        batch_id = request.data.get(BatchDetail.BATCH_ID)
        cases_data = request.data.get("cases", [])

        # Input validation
        if not batch_id:
            return Response({"error": "batch_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not cases_data:
            return Response({"error": "No cases provided"}, status=status.HTTP_400_BAD_REQUEST)

        output = []
        calculation_service = CalculationDataView()

        try:
            # Step 1: Extract garnishment types
            all_garnishment_types = calculation_service.get_all_garnishment_types(cases_data)
            if not all_garnishment_types:
                return Response({"error": "No valid garnishment types found"}, status=status.HTTP_400_BAD_REQUEST)

            logger.info(f"Processing batch {batch_id} with garnishment types: {all_garnishment_types}")

            # Step 2 & 3: Preload fees + config
            #gar_fees = calculation_service.preload_garnishment_fees()
            full_config_data = calculation_service.preload_config_data(all_garnishment_types)

            # Step 4: Process each case
            with ThreadPoolExecutor(max_workers=100) as executor:
                future_to_case = {}
                for case_info in cases_data:
                    if calculation_service.is_multi_garnishment_case(case_info):
                        case_types = calculation_service.get_case_garnishment_types(case_info)
                        case_config = calculation_service.filter_config_for_case(full_config_data, case_types)
                    else:
                        case_config = full_config_data

                    future = executor.submit(
                        calculation_service.calculate_garnishment_result,
                        case_info,
                        batch_id,
                        case_config
                    )
                    future_to_case[future] = case_info

                # Step 5: Collect results
                for future in as_completed(future_to_case):
                    case_info_original = future_to_case[future]
                    ee_id_for_log = case_info_original.get(EE.EMPLOYEE_ID, "N/A")

                    try:
                        result = future.result()
                        if result:
                            if calculation_service.is_multi_garnishment_case(case_info_original):
                                result['is_multi_garnishment'] = True
                                result['garnishment_types'] = list(
                                    calculation_service.get_case_garnishment_types(case_info_original)
                                )
                            output.append(result)
                        else:
                            logger.warning(f"No result returned for employee {ee_id_for_log}")
                    except Exception as e:
                        error_message = f"Error processing garnishment for employee {ee_id_for_log}: {str(e)}"
                        logger.error(error_message, exc_info=True)
                        output.append({
                            "employee_id": ee_id_for_log,
                            "error": error_message,
                            "status": status.HTTP_500_INTERNAL_SERVER_ERROR
                        })

        except Exception as e:
            logger.error(f"Critical error in batch processing {batch_id}: {str(e)}", exc_info=True)
            return Response({"error": f"Critical error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 6: Prepare response
        error_count = sum(1 for item in output if "error" in item)
        success_count = len(output) - error_count

        response_data = {
            "success": True,
            "message": "Batch processed successfully.",
            "status_code": status.HTTP_200_OK,
            "batch_id": batch_id,
            "processed_at": datetime.now(),
            "summary": {
                "total_cases": len(cases_data),
                "successful_cases": success_count,
                "failed_cases": error_count,
                "garnishment_types_processed": list(all_garnishment_types)
            },
            "results": output
        }

        # HTML vs JSON Response
        if request.accepted_renderer.format == 'html':
            formatted_json = json.dumps(response_data, indent=2, ensure_ascii=False)
            return Response(
                {"results": formatted_json},
                template_name=self.template_name,
                status=status.HTTP_200_OK
            )

        return Response(response_data, status=status.HTTP_200_OK)
