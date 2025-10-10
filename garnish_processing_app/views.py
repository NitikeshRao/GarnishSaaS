from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
from django.db import connection
from django.contrib import messages
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
import time
import os

def index(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of garnishment-calculator')
        else:
            return render(request,'garnish-process-app/index.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    
def batchProcess(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of batch-processing')
        else:
            return render(request,'garnish-process-app/batch-process/index.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    
def childSupportRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of child-support-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/child-support/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))


def garnishmentFeesRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of child-support-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/fees-rules/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))

def stateTaxLevyRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of state-tax-levy-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/state-tax-levy/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))

def creditorDeptRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of state-tax-levy-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/creditor-dept/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import connection
from django.contrib import messages
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
import time
# ...existing code...
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import status
import pandas as pd
import numpy as np
import random
import string
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from user_app.constants import (
    EmployeeFields as EE,
    GarnishmentTypeFields as GT,
    CalculationFields as CA,
    PayrollTaxesFields as PT,
    CalculationResponseFields as CR,
    ResponseMessages,
    BatchDetail
)
import os



def index(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of garnishment-calculator')
        else:
            return render(request,'garnish-process-app/index.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    
def batchProcess(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of batch-processing')
        else:
            return render(request,'garnish-process-app/batch-process/index.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    


def clean_data_for_json(data):
    """
    Recursively convert NaN to None and NumPy types to native Python types
    so the structure is JSON serializable.
    """
    if isinstance(data, dict):
        return {k: clean_data_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_data_for_json(item) for item in data]
    elif pd.isna(data):
        return None
    elif isinstance(data, (np.integer, np.floating)):
        return data.item()
    elif isinstance(data, (np.bool_, bool)):
        return bool(data)
    else:
        return data


class ConvertExcelToJsonView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    template_name = 'garnish-process-app/batch-process/index.html'

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='file',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="Excel file to upload"
            ),
            openapi.Parameter(
                name='title',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="Optional title"
            )
        ],
        responses={
            200: 'File uploaded and processed successfully',
            400: 'No file provided or missing key in data',
            422: 'Data value error',
            500: 'Internal server error'
        }
    )

    
    def get(self, request):
        # Render the page initially
        return Response({}, template_name=self.template_name)
    
    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Load Excel sheets
            garnishment_df = pd.read_excel(
                file, sheet_name='Garnishment Order')
            garnishment_df.columns = garnishment_df.columns.str.strip().str.lower()

            payroll_df = pd.read_excel(
                file, sheet_name='Payroll Batch', header=[0, 1])
            payroll_df.columns = payroll_df.columns.map(
                lambda x: '_'.join(str(i)
                                   for i in x) if isinstance(x, tuple) else x
            ).str.lower().str.strip()
            


            # Define column mapping dictionaries
            payroll_column_map = {
                'unnamed: 1_level_0_eeid': EE.EMPLOYEE_ID,
                'unnamed: 0_level_0_caseid': EE.CASE_ID,
                'unnamed: 2_level_0_payperiod': EE.PAY_PERIOD,
                'unnamed: 3_level_0_payrolldate': EE.PAYROLL_DATE,
                'earnings_grosspay': CA.GROSS_PAY,
                'earnings_wages': CA.WAGES,
                'earnings_commission&bonus': CA.COMMISSION_AND_BONUS,
                'earnings_nonaccountableallowances': CA.NON_ACCOUNTABLE_ALLOWANCES,
                'taxes_fedtaxamt': PT.FEDERAL_INCOME_TAX,
                'taxes_statetaxamt': PT.STATE_TAX,
                'taxes_local/othertaxes': PT.LOCAL_TAX,
                'taxes_medtax': PT.MEDICARE_TAX,
                'taxes_oasditax': PT.SOCIAL_SECURITY_TAX,
                'deductions_medicalinsurance': PT.MEDICAL_INSURANCE_PRETAX,
                'deductions_sdi': PT.CALIFORNIA_SDI,
                'deductions_lifeinsurance': PT.LIFE_INSURANCE,
                'taxes_wilmingtontax': PT.WILMINGTON_TAX,
                'deductions_uniondues': PT.UNION_DUES,
                'deductions_netpay': CA.NET_PAY,
                'deductions_famlitax': PT.FAMLI_TAX,
                'deductions_industrialinsurance': PT.INDUSTRIAL_INSURANCE,
            }

            garnishment_column_map = {
                'eeid': EE.EMPLOYEE_ID, 'caseid': EE.CASE_ID, 'ssn': EE.SSN,'ismultiplegarnishment': EE.IS_MULTIPLE_GARNISHMENT,
                'supportsecondfamily': EE.SUPPORT_SECOND_FAMILY, 'supports2ndfam': EE.SUPPORT_SECOND_FAMILY,
                'orderedamount': CA.ORDERED_AMOUNT, 'ordered$': CA.ORDERED_AMOUNT,
                'arrear>12weeks': EE.ARREARS_GREATER_THAN_12_WEEKS,
                'arrears_greater_than_12_weeks': EE.ARREARS_GREATER_THAN_12_WEEKS,
                'workstate': EE.WORK_STATE,  'homestate': EE.HOME_STATE,
                'no.ofexemptionsincludingself': EE.NO_OF_EXEMPTION_INCLUDING_SELF, 'no.ofexemptionincludingself': EE.NO_OF_EXEMPTION_INCLUDING_SELF,
                'garntype': EE.GARNISHMENT_TYPE,
                'arrearamount': CA.ARREAR_AMOUNT, 'arrear$': CA.ARREAR_AMOUNT,
                'no. ofdependentchild(underthe ageof16)': EE.NO_OF_DEPENDENT_CHILD,
                'isblind': EE.IS_BLIND, 'age': EE.AGE, 'spouseage': EE.SPOUSE_AGE,
                'filingstatus': EE.FILING_STATUS, 'isspouseblind': EE.IS_SPOUSE_BLIND,
                'statementofexemptionreceiveddate': EE.STATEMENT_OF_EXEMPTION_RECEIVED_DATE,
                'no.ofstudentdefaultloan': EE.NO_OF_STUDENT_DEFAULT_LOAN,
                # 'debt type': EE.DEBT_TYPE,
                'garnstartdate': EE.GARN_START_DATE,
                'consumerdebt': EE.CONSUMER_DEBT, 'non-consumerdebt': EE.NON_CONSUMER_DEBT}
                
            

            # Drop empty columns and rename
            garnishment_df.dropna(axis=1, how='all', inplace=True)
            payroll_df.dropna(axis=1, how='all', inplace=True)

            garnishment_df.rename(columns=garnishment_column_map, inplace=True)
            payroll_df.rename(columns=payroll_column_map, inplace=True)

            # # Strip 'case_id' fields before merging
            garnishment_df[EE.CASE_ID] = garnishment_df[EE.CASE_ID].str.strip()
            payroll_df[EE.CASE_ID] = payroll_df[EE.CASE_ID].str.strip()
            garnishment_df[EE.EMPLOYEE_ID] = garnishment_df[EE.EMPLOYEE_ID].str.strip()
            payroll_df[EE.EMPLOYEE_ID] = payroll_df[EE.EMPLOYEE_ID].str.strip()
            garnishment_df[EE.GARNISHMENT_TYPE] = garnishment_df[EE.GARNISHMENT_TYPE].str.strip()

            # Formated "mm-dd-yyyy"
            date_cols = [
                'statement_of_exemption_received_date', 'garn_start_date']
            garnishment_df[date_cols] = garnishment_df[date_cols].apply(
                lambda col: col.dt.strftime('%m-%d-%Y'))
            
            # Merge on both employee ID and case ID
            merged_df = pd.merge(payroll_df,
                    garnishment_df,
                    on=[EE.EMPLOYEE_ID, EE.CASE_ID],
                    how='left',
                    suffixes=('', '_garnishment')  
                )

            # Clean specific columns
            if EE.FILING_STATUS in merged_df.columns and merged_df[EE.FILING_STATUS].notna().any():
                merged_df[EE.FILING_STATUS] = merged_df[EE.FILING_STATUS].str.strip().str.lower(
                ).str.replace(" ", "_")
            else:
                merged_df[EE.FILING_STATUS] = None

            merged_df[EE.ARREARS_GREATER_THAN_12_WEEKS] = merged_df[EE.ARREARS_GREATER_THAN_12_WEEKS].astype(bool).apply(
                lambda x: True if str(x).lower() in ['true', '1',1,True,"Yes"] else False
            )

            merged_df[EE.SUPPORT_SECOND_FAMILY] = merged_df[EE.SUPPORT_SECOND_FAMILY].astype(bool).apply(
                lambda x: True if str(x).lower() in ['true', '1',1,True,"Yes"] else False
            )

            merged_df[EE.GARNISHMENT_TYPE] = merged_df[EE.GARNISHMENT_TYPE].str.strip().str.replace(' ', '_')

            # Generate dynamic batch ID
            batch_id = f"B{int(time.time() % 1000):03d}{random.choice(string.ascii_uppercase)}"

            # Build JSON structure
            output_json = {BatchDetail.BATCH_ID: batch_id, "cases": []}

            for ee_id, group in merged_df.groupby(f"{EE.EMPLOYEE_ID}"):
                first_row = group.iloc[0]

                is_multiple = str(first_row.get(EE.IS_MULTIPLE_GARNISHMENT, "")).strip().lower() in ["true", "1"]

                if is_multiple:
                    garnishment_data = []
                    for garn_type, sub_group in group.groupby(EE.GARNISHMENT_TYPE):
                        garn_type = garn_type.lower()
                        type_data = {
                            EE.GARNISHMENT_TYPE: garn_type,
                            "data": []
                        }

                        for _, row in sub_group.iterrows():
                            entry = {
                                EE.CASE_ID: row.get(EE.CASE_ID),
                                CA.ORDERED_AMOUNT: row.get(CA.ORDERED_AMOUNT),
                                CA.ARREAR_AMOUNT: row.get(CA.ARREAR_AMOUNT)
                            }
                                
                            type_data["data"].append(entry)

                        garnishment_data.append(type_data)

                    garnishment_orders = [item[EE.GARNISHMENT_TYPE].lower() for item in garnishment_data]

                else:
                    garn_type = first_row.get(EE.GARNISHMENT_TYPE).lower()
                    garnishment_data = [{
                        EE.GARNISHMENT_TYPE: garn_type,
                        "data": [
                            {
                                EE.CASE_ID: row.get(EE.CASE_ID),
                                CA.ORDERED_AMOUNT: row.get(CA.ORDERED_AMOUNT),
                                CA.ARREAR_AMOUNT: row.get(CA.ARREAR_AMOUNT)
                            }
                            for _, row in group.iterrows()
                        ]
                    }]

                    garnishment_orders = [garn_type]


                # Append employee data to output JSON
                output_json["cases"].append({
                    EE.EMPLOYEE_ID: ee_id,
                    EE.WORK_STATE: first_row.get(EE.WORK_STATE, "").strip(),
                    EE.NO_OF_EXEMPTION_INCLUDING_SELF: first_row.get(EE.NO_OF_EXEMPTION_INCLUDING_SELF),
                    EE.IS_MULTIPLE_GARNISHMENT: first_row.get(EE.IS_MULTIPLE_GARNISHMENT),
                    EE.NO_OF_STUDENT_DEFAULT_LOAN: first_row.get(EE.NO_OF_STUDENT_DEFAULT_LOAN),
                    EE.PAY_PERIOD: first_row.get(EE.PAY_PERIOD),
                    EE.FILING_STATUS: first_row.get(EE.FILING_STATUS),
                    CA.WAGES: first_row.get(CA.WAGES, 0),
                    CA.COMMISSION_AND_BONUS: first_row.get(CA.COMMISSION_AND_BONUS, 0),
                    CA.NON_ACCOUNTABLE_ALLOWANCES: first_row.get(CA.NON_ACCOUNTABLE_ALLOWANCES, 0),
                    CA.GROSS_PAY: first_row.get(CA.GROSS_PAY, 0),
                    PT.PAYROLL_TAXES: {
                        PT.FEDERAL_INCOME_TAX: first_row.get(PT.FEDERAL_INCOME_TAX, 0),
                        PT.SOCIAL_SECURITY_TAX: first_row.get(PT.SOCIAL_SECURITY_TAX, 0),
                        PT.MEDICARE_TAX: first_row.get(PT.MEDICARE_TAX, 0),
                        PT.STATE_TAX: first_row.get(PT.STATE_TAX, 0),
                        PT.LOCAL_TAX: first_row.get(PT.LOCAL_TAX, 0),
                        PT.UNION_DUES: first_row.get(PT.UNION_DUES, 0),
                        PT.WILMINGTON_TAX: first_row.get(PT.WILMINGTON_TAX, 0),
                        PT.MEDICAL_INSURANCE_PRETAX: first_row.get(PT.MEDICAL_INSURANCE_PRETAX, 0),
                        PT.INDUSTRIAL_INSURANCE: first_row.get(PT.INDUSTRIAL_INSURANCE, 0),
                        PT.LIFE_INSURANCE: first_row.get(PT.LIFE_INSURANCE, 0),
                        PT.CALIFORNIA_SDI: first_row.get(PT.CALIFORNIA_SDI, 0),
                        PT.FAMLI_TAX: first_row.get(PT.FAMLI_TAX, 0)
                    },
                    CA.NET_PAY: first_row.get(CA.NET_PAY),
                    EE.IS_BLIND: first_row.get(EE.IS_BLIND),
                    EE.STATEMENT_OF_EXEMPTION_RECEIVED_DATE: first_row.get(EE.STATEMENT_OF_EXEMPTION_RECEIVED_DATE),
                    EE.GARN_START_DATE: first_row.get(EE.GARN_START_DATE),
                    EE.NON_CONSUMER_DEBT: first_row.get(EE.NON_CONSUMER_DEBT),
                    EE.CONSUMER_DEBT: first_row.get(EE.CONSUMER_DEBT),
                    EE.AGE: first_row.get(EE.AGE),
                    EE.SPOUSE_AGE: first_row.get(EE.SPOUSE_AGE),
                    EE.IS_SPOUSE_BLIND: first_row.get(EE.IS_SPOUSE_BLIND),
                    EE.SUPPORT_SECOND_FAMILY: first_row.get(EE.SUPPORT_SECOND_FAMILY),
                    EE.NO_OF_DEPENDENT_CHILD: first_row.get(EE.NO_OF_DEPENDENT_CHILD, 0),
                    EE.ARREARS_GREATER_THAN_12_WEEKS: first_row.get(EE.ARREARS_GREATER_THAN_12_WEEKS),
                    EE.GARNISHMENT_DATA: garnishment_data,
                    EE.GARNISHMENT_ORDERS: garnishment_orders
                })
            output_json = clean_data_for_json(output_json)

            if request.accepted_renderer.format == 'html':
                # Format JSON for display
                import json
                formatted_json = json.dumps(output_json, indent=2, ensure_ascii=False)
                # Render the result into a template
                return Response(
                    {"results": formatted_json},
                    template_name='garnish-process-app/batch-process/index.html',
                    status=status.HTTP_200_OK
                )
            
            return Response(output_json, status=status.HTTP_200_OK)
        except KeyError as e:
            return Response({"error": f"Missing key in data: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": f"Data value error: {str(e)}"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


    
def childSupportRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of child-support-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/child-support/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    
def stateTaxLevyRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of state-tax-levy-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/state-tax-levy/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))

def creditorDeptRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of state-tax-levy-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/creditor-dept/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))