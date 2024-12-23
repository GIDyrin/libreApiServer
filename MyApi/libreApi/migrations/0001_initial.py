# Generated by Django 5.1.3 on 2024-11-17 12:16

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('author_name', models.TextField()),
                ('biography', models.TextField(blank=True, null=True)),
                ('image_path', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'db_table': 'authors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BookGenres',
            fields=[
                ('book_genre_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'book_genres',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bookmarks',
            fields=[
                ('bookmark_id', models.AutoField(primary_key=True, serialize=False)),
                ('page_number', models.IntegerField()),
            ],
            options={
                'db_table': 'bookmarks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_title', models.TextField()),
                ('book_year', models.IntegerField(blank=True)),
                ('description', models.CharField(blank=True, max_length=512)),
                ('book_path', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'books',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BooksRating',
            fields=[
                ('rating_id', models.AutoField(primary_key=True, serialize=False)),
                ('reviews_count', models.IntegerField()),
                ('avg_rate', models.FloatField()),
            ],
            options={
                'db_table': 'books_rating',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('genre_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'genres',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('review_text', models.CharField(max_length=2000)),
                ('review_rate', models.IntegerField()),
                ('review_date', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'reviews',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('about_user', models.TextField(blank=True, null=True)),
                ('profile_photo_path', models.CharField(blank=True, max_length=256, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
