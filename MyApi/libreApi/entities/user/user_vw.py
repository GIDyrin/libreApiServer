from django.http import FileResponse
from rest_framework import viewsets, generics, views, status
from .users_slz import *
from libreApi.models import Author, CustomUser
from rest_framework.response import Response
from django.core.files.storage import default_storage
import os
from datetime import datetime
from rest_framework.permissions import AllowAny

class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer


class Registration(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = DefaultUserSerializer(data=request.data)  # Десериализуем входящие данные
        if serializer.is_valid():  # Проверяем на валидность
            serializer.save()  # Сохраняем нового пользователя
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Возвращаем созданный объект
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Ошибка валидации
    
    
class UpdateInfo(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdatePersonalInfoSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        current_user = request.user
        
        # Получение пользователя, информацию которого мы обновляем
        instance = self.get_object()

        # Проверка, соответствует ли текущий пользователь пользователю, которого он пытается обновить
        if current_user != instance:
            return Response({"detail": "Недостаточно прав для обновления этой информации."}, status=status.HTTP_403_FORBIDDEN)
        
        # Сохраняем старый путь к изображению, если он существует
        old_profile_photo_path = instance.profile_photo_path

        # Обновляем данные пользователя с помощью сериализатора без изменения пути к фото
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Проверка на наличие нового изображения в запросе
        new_profile_photo = request.FILES.get('profile_photo', None)
           
        if new_profile_photo:
            file_type = new_profile_photo.content_type
            allowed_formats = {
                'image/jpeg': 'jpg',
                'image/png': 'png',
                'image/webp': 'webp',
            }    
        
        if file_type in allowed_formats:
            # Сохранение нового изображения
            file_path = default_storage.save(f'profile_photos/{instance.username + '-' + 'prphoto.' + allowed_formats[file_type]}', new_profile_photo)
            instance.profile_photo_path = file_path  # Сохраняем новый путь в базе данных
            if old_profile_photo_path and os.path.exists(old_profile_photo_path):
                os.remove(old_profile_photo_path)  # Удаляем старую картинку, если она существует

            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Неподдерживаемый формат файла."}, status=status.HTTP_400_BAD_REQUEST)
        
        
class GetUser(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = GetUserInfoSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Получаем данные из сериализатора
        user_data = serializer.data
        
        date_str = user_data['date_joined']
        date_joined = datetime.fromisoformat(date_str)

        # Форматируем дату в "день.месяц.год"
        formatted_date = date_joined.strftime("%d.%m.%Y")
        
        user_data['date_joined'] = formatted_date
        return Response(user_data, status=status.HTTP_200_OK)


class GetUserPhoto(generics.GenericAPIView):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        if user.profile_photo_path:
            return FileResponse(open(user.profile_photo_path, 'rb'), content_type = f'image/{user.profile_photo_path.split('.')[-1]}') 
        else:
            return Response({"detail": "Изображение не найдено."}, status=status.HTTP_404_NOT_FOUND)
        

    def delete(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)

        if request.user != user:
            return Response({"detail": "Ошибка доступа"}, status=status.HTTP_403_FORBIDDEN)
        
        if user.profile_photo_path:
            try:
                # Удаляем файл, если он существует
                os.remove(user.profile_photo_path)
                user.profile_photo_path = None  # Обнуляем поле в модели
                user.save()  # Сохраняем изменения в базе данных
                return Response({"detail": "Изображение удалено."}, status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"detail": f"Ошибка при удалении изображения.{e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Изображение не найдено."}, status=status.HTTP_404_NOT_FOUND)
        
        
class DeleteUser(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ToDeleteUser

    def delete(self, request, *args, **kwargs):
        user = self.get_object()  
        if request.user != user:
            return Response({"detail": "Ошибка доступа"}, status=status.HTTP_403_FORBIDDEN)
        
        photo = user.profile_photo_path
        self.perform_destroy(user)
        
        if photo:
            os.remove(photo)
        return Response({"detail": "Пользователь успешно удалён."}, status=status.HTTP_204_NO_CONTENT)