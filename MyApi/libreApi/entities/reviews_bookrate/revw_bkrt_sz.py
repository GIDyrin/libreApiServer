from libreApi.models import Reviews, BooksRating, Books
from rest_framework import serializers
from libreApi.entities.authors.authors_sz import AuthorsSerializer
from libreApi.entities.user.users_slz import GetUserInfoSerializer



class BookSerializer(serializers.ModelSerializer):
    author = AuthorsSerializer()
    class Meta:
        model = Books
        fields = ['book_id', 'book_title', 'book_year', 'description', 'author', 'book_path']
        
                  
class ReviewsSerializer(serializers.ModelSerializer):
  user = GetUserInfoSerializer()
  
  class Meta:
    model = Reviews
    fields = ['review_id','book', 'user', 'review_text', 'review_rate', 'review_date']
   
class ReviewPostSerializer(serializers.ModelSerializer):
   
  class Meta:
    model = Reviews
    fields = ['book', 'review_text', 'review_rate']
    
class ReviewsAndBookSerializer(serializers.ModelSerializer):
  book = BookSerializer()  # Включаем сериализатор для книги

  class Meta:
      model = Reviews
      fields = ['review_id', 'user', 'book', 'review_text', 'review_rate', 'review_date']
        
        
class BooksRatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = BooksRating
    fields = "__all__"
