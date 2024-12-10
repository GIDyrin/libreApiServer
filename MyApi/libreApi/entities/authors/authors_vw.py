from django.http import FileResponse
from rest_framework import generics, views, status
from .authors_sz import *
from libreApi.models import Author
from rest_framework.response import Response
from django.core.files.storage import default_storage
import os
from rest_framework.permissions import IsAuthenticated
from django.http import Http404



class RegUserAsAuthorView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        user = request.user  # Получаем текущего пользователя из запроса
        author_data = request.data

        # Проверяем есть ли уже автор с данным user_id
        if Author.objects.filter(user=user).exists():
            return Response({'detail': 'Автор уже зарегистрирован.'}, status=status.HTTP_400_BAD_REQUEST)

        # Сохраняем изображение при загрузке
        image = request.FILES.get('image')  # Получаем изображение из формата form-data
        print("Прикреплен")
        if image:
          file_type = image.content_type
          allowed_formats = {
              'image/jpeg': 'jpg',
              'image/png': 'png',
              'image/webp': 'webp',
          }    
          if file_type in allowed_formats:
            # Сохранение нового изображения
            file_path = default_storage.save(f'portraits/{user.username + '-portrait.' + allowed_formats[file_type]}', image)
            author_data['image_path'] = file_path  # Сохраняем новый путь в базе данных
          else:
            author_data['image_path'] = None
        
        # Устанавливаем user_id
        print(user.id)
        author_data['user'] = user.id
        serializer = self.get_serializer(data=author_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
      

class GetUpdateDeleteMeView(generics.GenericAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer

    def get_object(self):
        user_id = self.request.user.id
        try:
            return Author.objects.get(user=user_id)
        except Author.DoesNotExist:
            raise Http404("Author not found for the current user.")

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404 as e:
            return Response({"error": "Author not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            # Проверка на наличие нового изображения в запросе
            new_profile_photo = request.FILES.get('image', None)

            if new_profile_photo:
                file_type = new_profile_photo.content_type
                allowed_formats = {
                    'image/jpeg': 'jpg',
                    'image/png': 'png',
                    'image/webp': 'webp',
                }

                if file_type in allowed_formats:
                    file_path = default_storage.save(f'profile_photos/{instance.user.username}-prphoto.{allowed_formats[file_type]}', new_profile_photo)
                    old_profile_photo_path = instance.image_path
                    instance.image_path = file_path

                    # Удаляем старую фотографию, если она существует
                    if old_profile_photo_path:
                        os.remove(old_profile_photo_path)

                else:
                    return Response({"detail": "Неподдерживаемый формат файла."}, status=status.HTTP_400_BAD_REQUEST)

            self.perform_update(serializer)  # Сохраняем изменения
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
      

class AuthorPortraitView(generics.GenericAPIView):
    def get(self, request, author_id):
        author = Author.objects.get(author_id=author_id)
        if author.image_path:
            return FileResponse(open(author.image_path, 'rb'), content_type = f'image/{author.image_path.split('.')[-1]}') 
        else:
            return Response({"detail": "Изображение не найдено."}, status=status.HTTP_404_NOT_FOUND)
        
        
    def delete(self, request, author_id):
        author = Author.objects.get(author_id=author_id)

        if request.user != author.user:
            return Response({"detail": "Ошибка доступа"}, status=status.HTTP_403_FORBIDDEN)

        if author.image_path:
          try:
              # Удаляем файл, если он существует
              os.remove(author.image_path)
              author.image_path = None  # Обнуляем поле в модели
              author.save()  # Сохраняем изменения в базе данных
              return Response({"detail": "Изображение удалено."}, status=status.HTTP_204_NO_CONTENT)
          except Exception as e:
              return Response({"detail": f"Ошибка при удалении изображения.{e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response({"detail": "Изображение не найдено."}, status=status.HTTP_404_NOT_FOUND)
         
         
class GetAuthorsView(views.APIView):

    def get(self, request, author_id=None):
        # Если передан author_id, пытаемся получить конкретного автора
        if author_id is not None:
            return self.retrieve(request, author_id)

        # Если author_id не передан, то обрабатываем фильтрацию
        filter_str = request.query_params.get('filter', None)
        if filter_str:
            authors = Author.objects.filter(author_name__startswith=filter_str)  # Фильтруем по имени
        else:
            authors = Author.objects.all()  # Или получаем всех авторов

        serializer = AuthorsSerializer(authors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, author_id):
        try:
            author = Author.objects.get(author_id=author_id)  # Ищем автора по ID
            serializer = AuthorsSerializer(author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response({"detail": "Автор не найден."}, status=status.HTTP_404_NOT_FOUND)