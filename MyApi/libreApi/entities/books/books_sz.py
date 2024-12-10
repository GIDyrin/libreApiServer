from rest_framework import serializers
from libreApi.models import BookGenres, Books, Genres, Author
from django.core.files.storage import default_storage
from libreApi.entities.authors.authors_sz import AuthorsSerializer

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
    author = AuthorsSerializer()
    class Meta:
        model = Books
        fields = [ "book_id",
            "book_title",
            "book_year",
            "description",
            "book_path",
            "author"]


# Сериализатор для связей книги и жанров
class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenres
        fields = ['genre_id']  # Получаем полную информацию о жанре


class BookCreateSerializer(serializers.ModelSerializer):
    genres = serializers.CharField(write_only=True)  # Изменено на CharField
    book_file = serializers.FileField(write_only=True)

    class Meta:
        model = Books
        fields = ['book_title', 'book_year', 'description', 'genres', 'book_file']

    def validate_book_file(self, value):
        # Получаем расширение файла
        extension = value.name.split('.')[-1].lower()
        # Проверяем, что расширение совпадает с одним из допустимых типов
        if extension not in mime_types:
            raise serializers.ValidationError(f"Недопустимый формат файла. Поддерживаются: {', '.join(mime_types.keys())}.")
        return value

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', '')
        book_file = validated_data.pop('book_file', None)
        
        user_id = self.context['request'].user.id
        
        try:
            # Находим автора по ID пользователя
            author = Author.objects.get(user_id=user_id)
            validated_data['author'] = author  # Устанавливаем автора
        except Author.DoesNotExist:
            raise serializers.ValidationError("Автор с данным пользовательским ID не найден.")

        if book_file:
            # Указываем путь к файлу (например, загружаем в папку пользователя)
            validated_data['book_path'] = f'user_books/{book_file.name}'
        
        # Создаем объект книги
        book = Books.objects.create(**validated_data)

        # Обработка строки genres и добавление жанров в BookGenres
        if genres_data:
            genre_ids = [int(genre_id.strip()) for genre_id in genres_data.split(',')]
            for genre_id in genre_ids:
                try:
                    genre = Genres.objects.get(pk=genre_id)  # Пытаемся получить жанр по ID
                    BookGenres.objects.create(book=book, genre=genre)  # Создаем связь
                except Genres.DoesNotExist:
                    raise serializers.ValidationError(f"Жанр с ID {genre_id} не найден.")

        # Сохраняем файл на сервере, если файл присутствует
        if book_file:
            default_storage.save(validated_data['book_path'], book_file)

        return book