from rest_framework import serializers
from libreApi.models import Bookmarks


class BookmarkSerializer(serializers.ModelSerializer):
  class Meta:
    model = Bookmarks
    fields = '__all__'

