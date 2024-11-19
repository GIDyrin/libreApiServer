from rest_framework import serializers
from libreApi.models import Author, CustomUser

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


class UpdatePersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['about_user', 'profile_photo_path']
        
        
class GetUserInfoSerializer(serializers.ModelSerializer):
   class Meta:
      model = CustomUser
      fields = ['id', 'username', 'about_user', 'date_joined']
      

class ToDeleteUser(serializers.ModelSerializer):
  class Meta:
          model = CustomUser
          fields = '__all__'