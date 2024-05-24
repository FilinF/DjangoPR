from django.shortcuts import render
import pandas as pd
import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .application_service import handle_uploaded_file, delete_all_files
from .serializers import StudentSerializer
from django.views.decorators.csrf import csrf_exempt






class FileListView(APIView):
    def get(self, request, format=None):
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            return Response({'error': 'Upload directory does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        files = os.listdir(upload_dir)
        if not files:
            return Response({'error': 'No files found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'files': files}, status=status.HTTP_200_OK)


def display_excel(request, file_name):
    file_path = os.path.join("uploads", file_name)

    if not os.path.exists(file_path):
        return JsonResponse({'error': 'File not found'}, status=404)

    df = pd.read_excel(file_path)
    data = df.to_dict(orient='records')

    return JsonResponse(data, safe=False)

@csrf_exempt
def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['file']
        handle_uploaded_file(excel_file)  # Функция загрузки файла
        return redirect('display_excel', file_name=excel_file.name)
    return render(request, 'upload_excel.html')

@csrf_exempt
def delete_files_view(request):
    directory = os.path.join("uploads")  # Путь к каталогу с файлами
    success = delete_all_files(directory)
    if success:
        return JsonResponse({'message': 'files was deleted'})
    else:
        return JsonResponse({'error'}, status=500)

def button_view(request):
    return render(request, 'button.html')