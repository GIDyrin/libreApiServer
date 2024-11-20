from libreApi.models import Reviews, BooksRating
from rest_framework import serializers


class ReviewsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Reviews
    fields = ['review_id','book', 'review_text', 'review_rate', 'review_date']
    
    
    
class BooksRatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = BooksRating
    fields = "__all__"
