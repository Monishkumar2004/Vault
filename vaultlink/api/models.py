from django.db import models
import os 
import uuid
# Create your models here.


class Folder(models.Model):
    uid = models.UUIDField(primary_key=True, editable= False, default= uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)


def upload_path(instance, file_name):
    # instance is the current file object beiing saved
    # file_name is the original filename
    return os.path.join(str(instance.folder.uid), file_name)
    # Example: "f6a1a876/filename.pdf"


class Files(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=upload_path)
    created_at = models.DateTimeField(auto_now=True)
