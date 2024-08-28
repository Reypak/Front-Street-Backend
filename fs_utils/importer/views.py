from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from django.apps import apps
from .serializers import FileUploadSerializer

MODEL_APP_MAPPING = {
    'charge': 'fs_charges',
    'loan': 'fs_loans'
}


class ImportDataView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            model_name = serializer.validated_data['module']
            try:
                # Determine the app_label based on the model_name
                app_label = MODEL_APP_MAPPING.get(model_name)
                if not app_label:
                    return Response({"error": f"App label for model '{model_name}' not found."}, status=status.HTTP_400_BAD_REQUEST)
                # Dynamically get the model class based on model_name
                model = apps.get_model(
                    app_label=app_label,
                    model_name=model_name)
                if not model:
                    return Response({"error": f"Model '{model_name}' not found."}, status=status.HTTP_400_BAD_REQUEST)

                 # Get the field mapping from the model's method
                field_mapping = model().get_field_mapping()

                # Read the Excel file into a DataFrame
                df = pd.read_excel(file)

                for index, row in df.iterrows():
                    obj_data = {}
                    for excel_col, model_field in field_mapping.items():
                        if pd.notna(row.get(excel_col)):
                            obj_data[model_field] = row.get(excel_col)

                    # Create or update the object
                    obj, created = model.objects.get_or_create(
                        **obj_data, created_by=request.user)

                    if created:
                        print(f'{model_name} object created: {obj}')
                    else:
                        print(f'{model_name} object already exists: {obj}')

                # for index, row in df.iterrows():
                #     item, created = Charge.objects.get_or_create(
                #         name=row['name'],
                #         defaults={
                #             'amount': row['amount'],
                #             'type': row['type'],
                #             'description': row.get('description', ''),
                #         },
                #         created_by=request.user
                #     )

                #     if created:
                #         print(f'item {item.name} created')
                #     else:
                #         print(f'item {item.name} already exists')

                return Response({"message": "Data import completed successfully"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
