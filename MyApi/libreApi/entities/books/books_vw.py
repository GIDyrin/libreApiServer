from django.http import FileResponse
from django.db.models import Count
from rest_framework import viewsets, generics, views, status
from .books_sz import *
from libreApi.models import Books, BookGenres, Author
from rest_framework.response import Response
from django.core.files.storage import default_storage
import os
from ..authors.authors_sz import AuthorsSerializer
from rest_framework.pagination import PageNumberPagination

mime_types = {
    'fb2': 'application/x-fictionbook',
    'pdf': 'application/pdf',
    'epub': 'application/epub+zip',
    'mobi': 'application/x-mobipocket-ebook'
}

class BooksPagination(PageNumberPagination):
    page_size = 50  # Количество книг на странице
    page_size_query_param = 'page_size'  # Параметр в URL для указания количества элементов
    max_page_size = 100  # Максимально допустимое количество элементов на странице


class GetBookFile(generics.RetrieveAPIView):
    queryset = Books.objects.all() 
    serializer_class = BookSerializer  

    def retrieve(self, request, *args, **kwargs):
        book = self.get_object()
    
        if book.book_path:
            return FileResponse(open(book.book_path, 'rb'), content_type = f'{mime_types[book.book_path.split('.')[-1]]}') 
        else:
            return Response({"detail": "Изображение не найдено."}, status=status.HTTP_404_NOT_FOUND)
          
class GetBookInfo(generics.RetrieveAPIView):
    queryset = Books.objects.all()


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Получаем объект книги
        
        genres_list = [genre.genre for genre in BookGenres.objects.filter(book_id=instance.book_id)]
        # Возвращаем все поля, даже если их нет в Meta fields
        response_data = {
            "book_id": instance.book_id,
            "book_title": instance.book_title,
            "book_year": instance.book_year,
            "description": instance.description,
            "book_path": instance.book_path,
            "author": AuthorsSerializer(Author.objects.get(author_id=instance.author_id)).data,
            "genres": GenresSerializer(genres_list, many = True).data
        }
        return Response(response_data)


class PostBook(generics.CreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Проверка данных на валидность
        
        self.perform_create(serializer)  # Сохранение книги и жанров
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    
class DeleteMyBook(generics.DestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    
    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        
        check = Author.objects.get(user=request.user.id)
        if check == book.author:
            os.remove(book.book_path)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"details": "YOU CANNOT DELETE OTHER AUTHOR'S BOOK"}, status=status.HTTP_403_FORBIDDEN)
        
        
class GetBooksByAuthor(views.APIView):
    def get(self, request, author_id):
        filtered_books = Books.objects.filter(author=author_id)
       
        return Response(BookSerializer(filtered_books ,many = True).data, status=status.HTTP_200_OK)
    
    
class GetBooksByGenres(views.APIView):
    pagination_class = BooksPagination
    
    def get(self, request):
        filter_str = request.query_params.get('genre_ids')
        
        if not filter_str:
            return Response({"error": "genre_ids parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем список идентификаторов жанров
        genre_ids = list(map(int, filter_str.split(',')))
        
        # Фильтруем книги по жанрам и считаем количество совпадений
        queryset = (
            Books.objects
            .filter(bookgenres__genre__in=genre_ids)
            .annotate(num_genres=Count('bookgenres__genre'))
            .filter(num_genres=len(genre_ids))
        )

         # Применяем пагинацию
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = BookSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        