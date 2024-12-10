from rest_framework import views, generics
from rest_framework.exceptions import ValidationError, PermissionDenied
from .revw_bkrt_sz import *
from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response


class PostReviewView(generics.CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewPostSerializer

    def perform_create(self, serializer):
        try:
            # Сохраняем отзыв с пользователем из запроса
            review = serializer.save(user=self.request.user)
        except IntegrityError:
            # Если произошла ошибка уникальности, бросаем ValidationError
            raise ValidationError({'detail': 'Отзыв для этой книги уже существует от данного пользователя.'})

        book = review.book
        
        # Попробуем получить существующую запись BooksRating для книги
        books_rating, created = BooksRating.objects.get_or_create(book=book, defaults={'reviews_count': 0, 'avg_rate': 0.0})
        
        books_rating.reviews_count += 1
        
        # Обновляем средний рейтинг
        total_rating = books_rating.avg_rate * (books_rating.reviews_count - 1) + review.review_rate
        books_rating.avg_rate = total_rating / books_rating.reviews_count
        
        books_rating.save()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        
class DeleteReviewView(generics.DestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user:
            raise PermissionDenied("Вы не можете удалить этот отзыв.")
        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
      
class BookReviewsView(generics.ListAPIView):
    serializer_class = ReviewsSerializer
    
    def get_queryset(self):
        bookId = self.kwargs['pk']
        return  Reviews.objects.filter(book=bookId)
    
    
class UserReviewsView(generics.ListAPIView):
    serializer_class = ReviewsAndBookSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Reviews.objects.filter(user__id=user_id)