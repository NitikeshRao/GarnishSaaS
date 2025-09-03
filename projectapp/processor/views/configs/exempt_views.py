from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from processor.models import ExemptConfig
from processor.serializers import ExemptConfigWithThresholdSerializer
import logging
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.exceptions import ValidationError
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import json, logging
from datetime import datetime
from processor.models import ThresholdCondition
from processor.serializers import ThresholdConditionSerializer
from processor.garnishment_library import ResponseHelper
import logging
from processor.models import ExemptRule
from processor.serializers import ExemptRuleSerializer
from processor.garnishment_library.utils.response import ResponseHelper  
import logging


logger = logging.getLogger(__name__)


class ExemptConfigAPIView(APIView):
    """
    API view for CRUD operations on ExemptConfig
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Response("ExemptConfig data fetched successfully", ExemptConfigWithThresholdSerializer(many=True)),
            404: "ExemptConfig not found",
            500: "Internal server error"
        }
    )
    def get(self, request, pk=None):
        try:
            if pk:
                config = ExemptConfig.objects.get(pk=pk)
                serializer = ExemptConfigWithThresholdSerializer(config)
                return Response(serializer.data, status=status.HTTP_200_OK)
            configs = ExemptConfig.objects.select_related('state','pay_period','garnishment_type').all()
            serializer = ExemptConfigWithThresholdSerializer(configs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ExemptConfig.DoesNotExist:
            return Response({"error": "ExemptConfig not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unexpected error in GET")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=ExemptConfigWithThresholdSerializer)
    def post(self, request):
        try:
            serializer = ExemptConfigWithThresholdSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error creating ExemptConfig")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(request_body=ExemptConfigWithThresholdSerializer)
    def put(self, request, pk=None):
        if not pk:
            return Response({"error": "pk required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            config = ExemptConfig.objects.get(pk=pk)
            serializer = ExemptConfigWithThresholdSerializer(config, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ExemptConfig.DoesNotExist:
            return Response({"error": "ExemptConfig not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Error updating ExemptConfig")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"error": "pk required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            config = ExemptConfig.objects.get(pk=pk)
            config.delete()
            return Response({"message": "Deleted successfully"}, status=status.HTTP_200_OK)
        except ExemptConfig.DoesNotExist:
            return Response({"error": "ExemptConfig not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Error deleting ExemptConfig")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExemptRuleView(APIView):
    """Handles ExemptRule CRUD API with Multi-Type Support"""
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    template_name = 'garnish-process-app/garnish-rules/creditor-dept/index.html'  

    # -------------------- GET --------------------
    @swagger_auto_schema(
        responses={
            200: openapi.Response("Exempt rules fetched successfully", ExemptRuleSerializer),
            404: "Rule not found",
            500: "Internal server error"
        }
    )
    def get(self, request, pk=None):
        """Render rules list or single rule (HTML + JSON)."""
        try:
            if pk:
                rule = ExemptRule.objects.get(pk=pk)
                serializer = ExemptRuleSerializer(rule)
                data = serializer.data
            else:
                rules = ExemptRule.objects.all()
                serializer = ExemptRuleSerializer(rules, many=True)
                data = serializer.data

            response_data = {
                "success": True,
                "message": "Rules fetched successfully",
                "status_code": status.HTTP_200_OK,
                "fetched_at": datetime.now(),
                "results": data,
            }

            if request.accepted_renderer.format == "html":
                formatted_json = json.dumps(response_data, indent=2, ensure_ascii=False)
                return Response({"results": formatted_json}, template_name=self.template_name)

            return Response(response_data, status=status.HTTP_200_OK)

        except ExemptRule.DoesNotExist:
            return Response(
                {"success": False, "message": "Rule not found", "status_code": status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.exception("Unexpected error in GET ExemptRuleView")
            return Response(
                {"success": False, "message": f"Internal server error: {str(e)}", "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    # -------------------- POST --------------------
    @swagger_auto_schema(
        request_body=ExemptRuleSerializer,
        responses={
            201: openapi.Response("Rule created successfully", ExemptRuleSerializer),
            400: "Invalid data",
            500: "Internal server error"
        }
    )
    def post(self, request, *args, **kwargs):
        """Create a new ExemptRule (HTML + JSON)."""
        serializer = ExemptRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "success": True,
                "message": "Rule created successfully",
                "status_code": status.HTTP_201_CREATED,
                "created_at": datetime.now(),
                "results": serializer.data,
            }
            if request.accepted_renderer.format == "html":
                return Response({"results": json.dumps(response_data, indent=2)}, template_name=self.template_name)
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(
            {"success": False, "message": "Invalid data", "errors": serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -------------------- PUT --------------------
    @swagger_auto_schema(
        request_body=ExemptRuleSerializer,
        responses={
            200: openapi.Response("Rule updated successfully", ExemptRuleSerializer),
            400: "Invalid data",
            404: "Rule not found",
            500: "Internal server error"
        }
    )
    def put(self, request, pk=None):
        """Update existing ExemptRule (HTML + JSON)."""
        if not pk:
            return Response({"error": "Rule ID required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rule = ExemptRule.objects.get(pk=pk)
        except ExemptRule.DoesNotExist:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExemptRuleSerializer(rule, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "success": True,
                "message": "Rule updated successfully",
                "status_code": status.HTTP_200_OK,
                "updated_at": datetime.now(),
                "results": serializer.data,
            }
            if request.accepted_renderer.format == "html":
                return Response({"results": json.dumps(response_data, indent=2)}, template_name=self.template_name)
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(
            {"success": False, "message": "Invalid data", "errors": serializer.errors, "status_code": status.HTTP_400_BAD_REQUEST},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # -------------------- DELETE --------------------
    @swagger_auto_schema(
        responses={
            200: "Rule deleted successfully",
            404: "Rule not found",
            500: "Internal server error"
        }
    )
    def delete(self, request, pk=None):
        """Delete rule (HTML + JSON)."""
        if not pk:
            return Response({"error": "Rule ID required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rule = ExemptRule.objects.get(pk=pk)
            rule.delete()
            response_data = {
                "success": True,
                "message": "Rule deleted successfully",
                "status_code": status.HTTP_200_OK,
            }
            if request.accepted_renderer.format == "html":
                return Response({"results": json.dumps(response_data, indent=2)}, template_name=self.template_name)
            return Response(response_data, status=status.HTTP_200_OK)
        except ExemptRule.DoesNotExist:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Unexpected error in DELETE ExemptRuleView")
            return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ThresholdConditionAPI(APIView):
    """
    CRUD API for ThresholdCondition
    """

    @swagger_auto_schema(
        responses={
            200: openapi.Response('Threshold conditions fetched successfully', ThresholdConditionSerializer(many=True)),
            404: 'Threshold condition not found',
            400: 'Invalid input',
            500: 'Internal server error'
        }
    )
    def get(self, request, pk=None):
        try:
            if pk:
                try:
                    condition = ThresholdCondition.objects.get(id=pk)
                    serializer = ThresholdConditionSerializer(condition)
                    return ResponseHelper.success_response(
                        f'Threshold condition with id "{pk}" fetched successfully',
                        serializer.data
                    )
                except ThresholdCondition.DoesNotExist:
                    return ResponseHelper.error_response(
                        f'Threshold condition with id "{pk}" not found',
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            else:
                conditions = ThresholdCondition.objects.all()
                serializer = ThresholdConditionSerializer(conditions, many=True)
                return ResponseHelper.success_response('All threshold conditions fetched successfully', serializer.data)
        except ValidationError as e:
            return ResponseHelper.error_response(f"Invalid input: {str(e)}", status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Unexpected error in GET method (ThresholdCondition)")
            return ResponseHelper.error_response("An unexpected error occurred.", str(e),
                                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=ThresholdConditionSerializer,
        responses={
            201: openapi.Response('Threshold condition created successfully', ThresholdConditionSerializer),
            400: 'Invalid data',
            500: 'Internal server error'
        }
    )
    def post(self, request):
        try:
            serializer = ThresholdConditionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHelper.success_response('Threshold condition created successfully',
                                                       serializer.data,
                                                       status_code=status.HTTP_201_CREATED)
            else:
                return ResponseHelper.error_response('Invalid data', serializer.errors,
                                                     status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error creating ThresholdCondition")
            return ResponseHelper.error_response('Internal server error while creating data', str(e),
                                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        request_body=ThresholdConditionSerializer,
        responses={
            200: openapi.Response('Threshold condition updated successfully', ThresholdConditionSerializer),
            400: 'ID is required in URL to update data or invalid data',
            404: 'Threshold condition not found',
            500: 'Internal server error'
        }
    )
    def put(self, request, pk=None):
        if not pk:
            return ResponseHelper.error_response('ID is required in URL to update data',
                                                 status_code=status.HTTP_400_BAD_REQUEST)
        try:
            condition = ThresholdCondition.objects.get(id=pk)
        except ThresholdCondition.DoesNotExist:
            return ResponseHelper.error_response(f'Threshold condition with id "{pk}" not found',
                                                 status_code=status.HTTP_404_NOT_FOUND)
        try:
            serializer = ThresholdConditionSerializer(condition, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return ResponseHelper.success_response('Threshold condition updated successfully', serializer.data)
            else:
                return ResponseHelper.error_response('Invalid data', serializer.errors,
                                                     status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception("Error updating ThresholdCondition")
            return ResponseHelper.error_response('Internal server error while updating data', str(e),
                                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            200: 'Threshold condition deleted successfully',
            400: 'ID is required in URL to delete data',
            404: 'Threshold condition not found',
            500: 'Internal server error'
        }
    )
    def delete(self, request, pk=None):
        if not pk:
            return ResponseHelper.error_response('ID is required in URL to delete data',
                                                 status_code=status.HTTP_400_BAD_REQUEST)
        try:
            condition = ThresholdCondition.objects.get(id=pk)
            condition.delete()
            return ResponseHelper.success_response(f'Threshold condition with id "{pk}" deleted successfully')
        except ThresholdCondition.DoesNotExist:
            return ResponseHelper.error_response(f'Threshold condition with id "{pk}" not found',
                                                 status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Error deleting ThresholdCondition")
            return ResponseHelper.error_response('Internal server error while deleting data', str(e),
                                                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)