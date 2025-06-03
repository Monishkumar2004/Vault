from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .serializers import *
from users.models import CustomUser

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def ops_user_view(request):
    return render(request, 'ops_user_page.html')



class FileUpload(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "List files endpoint"})

    def post(self, request):    
        # Check if user is ops_user
        if request.user.user_type != 1:  # 1 represents ops_user
            raise PermissionDenied("Only operations users can upload files.")
            
        try:
            data = request.data

            serializer = FileListSerializer(data=data)

            if serializer.is_valid():
                result = serializer.save()
                return Response(
                    {
                        'status': 200,
                        'message': 'files uploaded successfully',
                        'data': {
                            'files': result['files'],
                            'folder': result['folder']
                        }
                    }
                )
            
            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(f"Exception in FileUpload view: {str(e)}")
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FileList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if user is client
        if request.user.user_type != 2:  # 2 represents client
            raise PermissionDenied("Only clients can view files.")
            
        try:
            # Get all files from all folders
            files = Files.objects.all().order_by('-created_at')
            file_list = []
            folders = {}  # To group files by folder
            
            for file in files:
                folder_uid = str(file.folder.uid)
                if folder_uid not in folders:
                    folders[folder_uid] = {
                        'files': [],
                        'zip_url': f'/media/zip/{folder_uid}.zip'
                    }
                
                folders[folder_uid]['files'].append({
                    'id': file.id,
                    'name': file.file.name.split('/')[-1],  # Get just the filename
                    'url': file.file.url,
                    'created_at': file.created_at
                })
                
            return Response({
                'status': 200,
                'data': {
                    'folders': folders
                }
            })
            
        except Exception as e:
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)