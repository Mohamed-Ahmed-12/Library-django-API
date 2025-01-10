from rest_framework import serializers
from .models import Book , Author
from django.contrib.auth.models import User 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email', "password"]
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure password is write-only not appear in other Serializer that use UserSerializer
        }
    
    #@override create method to hashed the password
    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance   


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        
