from rest_framework import serializers
from libreApi.models import Author

class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
