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
    path('api/v1/registration/', RegistrationView.as_view()),
    
    #USER GETINFO/PHOTO, UPDATE INFO/PHOTO, DELETE USER/PHOTO
    path('api/v1/user/update/<int:pk>/', UpdateInfoView.as_view()),
    path('api/v1/user/<int:pk>/', GetUserView.as_view()),
    path('api/v1/user/<int:user_id>/photo/', GetUserPhotoView.as_view()),
    path('api/v1/user/delete/', DeleteUserView.as_view(), name='delete-user'), 
    path('api/v1/user/me/', GetMyProfileView.as_view()),
    
    #AUTHORS: POST UserRegistrateASAuthor, 
    path('api/v1/authors/new/', RegUserAsAuthorView.as_view()),
    path('api/v1/authors/me/', GetUpdateDeleteMeView.as_view()),
    path('api/v1/authors/<int:author_id>/portrait/', AuthorPortraitView.as_view()),
    path('api/v1/authors/', GetAuthorsView.as_view(),),  
    path('api/v1/authors/<int:author_id>/', GetAuthorsView.as_view()), 
    
    #BOOKS
    path('api/v1/books/download/<int:pk>/', GetBookFileView.as_view()),
    path('api/v1/books/<int:pk>/', GetBookInfoView.as_view()),
    path('api/v1/books/new/', PostBookView.as_view()),
    path('api/v1/books/me/<int:pk>/', DeleteMyBookView.as_view()),
    path('api/v1/books/byauthor/<int:author_id>/', GetBooksByAuthorView.as_view()),
    path('api/v1/books/', GetBooksByGenresView.as_view()),
    
    
    #BOOKMARKS
    path('api/v1/bookmarks/me/<int:pk>/', BookmarkRUDView.as_view()),
    path('api/v1/bookmarks/me/', UsersBookmarksView.as_view()),
    path('api/v1/bookmarks/me/new/', CreateBookmarkView.as_view()),
    
    #REVIEWS
    path('api/v1/reviews/new/', PostReviewView.as_view()),
    path('api/v1/reviews/book/<int:pk>/',BookReviewsView.as_view()),
    path('api/v1/reviews/delete/<int:pk>/', DeleteReviewView.as_view()),
    path('api/v1/reviews/user/<int:user_id>/', UserReviewsView.as_view()),
]


