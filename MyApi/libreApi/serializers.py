from rest_framework import serializers
from .models import Author, CustomUser


class AuthorsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author
    fields = '__all__'
    
    
class DefaultUserSerializer(serializers.ModelSerializer):
  class Meta:
      model = CustomUser
      fields = ['id', 'username', 'email', 'password']
      extra_kwargs = {'password': {'write_only': True}}  # Убедитесь, что пароль только для записи

  def create(self, validated_data):
      user = CustomUser(
          username=validated_data['username'],
          email=validated_data['email'],
        )
      user.set_password(validated_data['password']) 
      user.save()
      return user

