
from rest_framework import serializers
from employee.models import IWOPDFFiles

class IWOPDFFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IWOPDFFiles
        fields = ['id', 'name', 'pdf_url', 'uploaded_at']

