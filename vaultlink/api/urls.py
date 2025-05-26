from django.urls import path
from .views import ops_user_view, FileUpload, FileList

urlpatterns = [
      path('ops_user/', ops_user_view, name = "ops_user_path"),

      path('file-upload/', FileUpload.as_view(), name='file_upload_api'),
      path('file-list/', FileList.as_view(), name='file_list_api'),
]
