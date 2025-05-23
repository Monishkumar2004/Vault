from django.urls import path
from .views import ops_user_view, FileUpload

urlpatterns = [
      path('ops_user/', ops_user_view, name = "ops_user_path"),

      path('file-upload/', FileUpload.as_view(), name='file_upload_api'),

]
