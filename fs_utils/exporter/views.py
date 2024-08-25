import openpyxl
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from datetime import date
from fs_loans.models import Loan
from fs_loans.serializers import *


class ExportToExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Fetch data from the database
        queryset = Loan.objects.all()
        serializer = LoanListSerializer(queryset, many=True)

        # Create a new Excel workbook and add a sheet
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Your Data'

        # Add column headers
        headers = list(serializer.data[0].keys())
        worksheet.append(headers)

        # Add data rows
        for data in serializer.data:
            worksheet.append(list(data.values()))

        # Generate filename
        filename = f'excel-data-{date.today()}.xlsx'

        # Prepare response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        # Save workbook to response
        workbook.save(response)
        return response
