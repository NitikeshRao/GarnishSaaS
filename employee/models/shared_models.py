from django.db import models

class IWOPDFFiles(models.Model):
    name = models.CharField(max_length=255)
    pdf_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "iwo_pdf_files"


class IWO_Details_PDF(models.Model):
    IWO_ID = models.AutoField(primary_key=True)
    cid = models.CharField(max_length=250)
    ee_id = models.CharField(max_length=250)
    IWO_Status = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "iwo_details_pdf"

class setting(models.Model):
    employer_id = models.IntegerField()
    modes = models.BooleanField()
    visibilitys = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "setting"

