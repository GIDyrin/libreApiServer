from django.db import models
from django.utils import timezone

class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # Используем AutoField для автоинкремента
    email = models.EmailField(unique=True, max_length=255)  # Поле для хранения уникального email
    password_hash = models.CharField(max_length=256)  # Поле для хранения хэшированного пароля
    username = models.CharField(unique=True, max_length=30)  # Поле для уникального имени пользователя
    about_user = models.CharField(max_length=1024, blank=True, null=True)  # Поле для информации о пользователе
    profile_photo_path = models.CharField(max_length=256, blank=True, null=True)  # Путь к профилю фотографии
    registration_time = models.DateTimeField(default=timezone.now)  # Время регистрации пользователя

    class Meta:
      managed = False
      db_table = 'users'
      
    def __str__(self):
        return self.username  # Возвращаем имя пользователя для удобства
      

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)  # serial, auto-incrementing primary key
    author_name = models.TextField(null=False)  # текст, не может быть NULL
    biography = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')  # Связь с пользователем
    image_path = models.CharField(max_length=256, blank=True, null=True)  

    class Meta:
      managed = False
      db_table = 'authors'  # Имя таблицы в базе данных

    def __str__(self):
        return self.author_name  # Удобное отображение имени автора


class Genres(models.Model):
  genre_id = models.AutoField(primary_key=True)
  genre_name = models.CharField(max_length=50, null=False)
  
  class Meta:
      db_table = 'genres'
      managed = False
      
  def __str__(self):
          return self.genre_name  # Возвращаем имя пользователя для удобства
   
        
class Books(models.Model):
  book_id = models.AutoField(primary_key=True)
  book_title = models.TextField(null=False)
  book_year = models.IntegerField(blank=True)
  description = models.CharField(max_length=512, blank=True)
  author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
  book_path = models.CharField(max_length=256, null=False)
  
  class Meta:
      db_table = 'books'
      managed = False
  
  def __str__(self):
    return self.book_title
  
  
class BooksRating(models.Model):
  rating_id = models.AutoField(primary_key=True)
  book = models.ForeignKey(Books, on_delete=models.CASCADE, null=False, unique=True)
  reviews_count = models.IntegerField(null=False)
  avg_rate = models.FloatField(null=False)
  
  def __str__(self):
    return self.book.book_title
  
  class Meta:
      db_table = 'books_rating'
      managed = False
      

class BookGenres(models.Model):
  book_genre_id = models.AutoField(primary_key=True)
  book = models.ForeignKey(Books, on_delete=models.CASCADE, null=False)
  genre = models.ForeignKey(Genres, on_delete=models.CASCADE, null=False)
  
  def __str__(self):
    return self.book.book_title + self.genre.genre_name
  
  class Meta:
      db_table = 'book_genres'
      managed = False
      
      
class Reviews(models.Model):
  review_id = models.AutoField(primary_key=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  book = models.ForeignKey(Books, on_delete=models.CASCADE, null=False)
  review_text = models.CharField(max_length=2000, null=False)
  review_rate = models.IntegerField(null=False)
  review_date = models.DateField(auto_now=True)
  
  def __str__(self):
    return self.review_id
  
  class Meta:
      db_table = 'reviews'
      managed = False
      
      
class Bookmarks(models.Model):
  bookmark_id = models.AutoField(primary_key=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
  book = models.ForeignKey(Books, on_delete=models.CASCADE, null=False)
  page_number = models.IntegerField(null=False)
  
  class Meta:
      db_table = 'bookmarks'
      managed = False
      
      
#class AuthUsers(models.Model):
