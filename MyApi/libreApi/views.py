from django.shortcuts import render
from rest_framework import viewsets, generics, views, status
from .serializers import AuthorsSerializer, DefaultUserSerializer
from .models import Author
from rest_framework.response import Response
from django.contrib.auth.models import User as DefaultUser



class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer


class Registration(views.APIView):
    def post(self, request):
        serializer = DefaultUserSerializer(data=request.data)  # Десериализуем входящие данные
        if serializer.is_valid():  # Проверяем на валидность
            serializer.save()  # Сохраняем нового пользователя
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Возвращаем созданный объект
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Ошибка валидации