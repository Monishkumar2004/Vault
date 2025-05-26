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


# @method_decorator(csrf_exempt, name='dispatch')
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