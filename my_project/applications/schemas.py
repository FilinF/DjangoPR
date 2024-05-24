from drf_yasg.openapi import Schema, TYPE_FILE

class UploadExcelSchema(Schema):
    type = TYPE_FILE
    description = "Excel file to upload"