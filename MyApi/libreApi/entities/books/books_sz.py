from rest_framework import serializers
from libreApi.models import BookGenres, Books, Genres
from django.core.files.storage import default_storage

mime_types = {
    'fb2': 'application/x-fictionbook',
    'pdf': 'application/pdf',
    'epub': 'application/epub+zip',
    'mobi': 'application/x-mobipocket-ebook'
}

# Сериализатор для жанров
class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ['genre_name']


# Сериализатор для книги
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


# Сериализатор для связей книги и жанров
class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenres
        fields = ['genre_id']  # Получаем полную информацию о жанре


class BookCreateSerializer(serializers.ModelSerializer):
    genres = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Genres.objects.all()),
        write_only=True
    )
    book_file = serializers.FileField(write_only=True)

    class Meta:
        model = Books
        fields = ['book_title', 'book_year', 'description', 'author', 'genres', 'book_file']

    def validate_book_file(self, value):
        # Получаем расширение файла
        extension = value.name.split('.')[-1].lower()
        # Проверяем, что расширение совпадает с одним из допустимых типов
        if extension not in mime_types:
            raise serializers.ValidationError(f"Недопустимый формат файла. Поддерживаются: {', '.join(mime_types.keys())}.")
        return value

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        book_file = validated_data.pop('book_file', None)

        if book_file:
            # Указываем путь к файлу
            validated_data['book_path'] = f'user_books/{book_file.name}'
        
        # Создаем объект книги
        book = Books.objects.create(**validated_data)

        # Добавляем жанры в BookGenres
        for genre in genres_data:
            BookGenres.objects.create(book=book, genre=genre)

        # Сохраняем файл на сервере
        if book_file:
          default_storage.save(validated_data['book_path'], book_file)

        return book
      
      


