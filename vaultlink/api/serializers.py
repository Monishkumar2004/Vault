from rest_framework import serializers
from .models import Folder, Files
import shutil

class FileSerializer(serializers.Serializer):

    class Meta:
        model = Files
        fields = '__all__'

class FileListSerializer(serializers.Serializer):
    
    files = serializers.ListField(
        child=serializers.FileField(max_length=10000, allow_empty_file=False, use_url=False),
        required=True,
        allow_empty=False
    )

    def validate_files(self, files):
        if not isinstance(files, list):
            files = [files]  # Convert single file to list
        allowed_extensions = ['pptx', 'docx', 'xlsx', 'pdf']
        # allowed_extensions = ['pptx', 'docx', 'xlsx']
        for file in files:
            ext = file.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise serializers.ValidationError(f"File type '{ext}' is not supported.")
        return files

    def zip_files(self, folder):
        shutil.make_archive(f'media/zip/{folder}', 'zip', f'media/{folder}')


    def create(self, validated_data):

        folder = Folder.objects.create()

        files = validated_data.get('files', [])

        if not isinstance(files, list):
            files = [files]  # Convert single file to list

        files_objs = []

        for file in files:
            files_obj = Files.objects.create(folder = folder, file = file)


            files_objs.append(files_obj)
        self.zip_files(folder.uid)

        return {
            'files': [{'id': f.id, 'file': f.file.name} for f in files_objs],
            'folder': str(folder.uid),
            'message': 'Files uploaded and zipped successfully'
        }
