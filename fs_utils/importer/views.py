from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

from fs_charges.models import Charge
from .serializers import FileUploadSerializer


class ImportDataView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            try:
                df = pd.read_csv(file)

                for index, row in df.iterrows():
                    item, created = Charge.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'amount': row['amount'],
                            'type': row['type'],
                            'description': row.get('description', ''),
                        },
                        created_by=request.user
                    )

                    if created:
                        print(f'item {item.name} created')
                    else:
                        print(f'item {item.name} already exists')

                return Response({"message": "Data import completed successfully"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
