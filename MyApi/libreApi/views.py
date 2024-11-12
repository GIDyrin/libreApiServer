from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import AuthorsSerializer
from .models import Author

class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorsSerializer
