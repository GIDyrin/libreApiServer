"""
URL configuration for MyApi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from libreApi.entities.export_views import *

router = DefaultRouter()




urlpatterns = [
    #AUTHORIZATION AND REGISTRATION
    #POST api/v1/auth/token/login (username:,password:, or)
    #POST api/v1/registration (email;username;password; optional(first_name, last_name))
    path('admin/', admin.site.urls),
    path('api/v1/', include('rest_framework.urls')),
    path('api/v1/auth', include('djoser.urls')),
    path('api/v1/', include(router.urls)),
    re_path(r'^api/v1/auth/', include('djoser.urls.authtoken')),
    path('api/v1/registration', Registration.as_view()),
    
    #USER GETINFO/PHOTO, UPDATE INFO/PHOTO, DELETE USER/PHOTO
    path('api/v1/user/update/<int:pk>', UpdateInfo.as_view()),
    path('api/v1/user/<int:pk>', GetUser.as_view()),
    path('api/v1/user/<int:user_id>/photo/', GetUserPhoto.as_view()),
    path('api/v1/users/<int:pk>/', DeleteUser.as_view(), name='delete-user'), 
    
    #AUTHORS: POST UserRegistrateASAuthor, 
    path('api/v1/authors/new/', RegUserAsAuthor.as_view()),
    path('api/v1/authors/me/', UpdateDeleteMe.as_view()),
    path('api/v1/authors/<int:author_id>/portrait/', AuthorPortrait.as_view()),
    path('api/v1/authors/', GetAuthors.as_view(),),  
    path('api/v1/authors/<int:author_id>/', GetAuthors.as_view()), 
    
    #BOOKS
    path('api/v1/books/download/<int:pk>/', GetBookFile.as_view()),
    path('api/v1/books/<int:pk>/', GetBookInfo.as_view()),
    path('api/v1/books/new', PostBook.as_view()),
    path('api/v1/books/me/<int:pk>/', DeleteMyBook.as_view()),
    path('api/v1/books/byauthor/<int:author_id>/', GetBooksByAuthor.as_view()),
    path('api/v1/books/', GetBooksByGenres.as_view())
]


