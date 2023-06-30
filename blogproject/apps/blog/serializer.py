from rest_framework import serializers
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True,max_length=255,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(max_length=65,write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(max_length=65,write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username','password','password2','email','first_name','last_name')
        extra_kwargs = {
           'first_name':{'required':True},
           'last_name':{'required':True}
        } 

    def validate(self,attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
          username=validated_data['username'],
          email=validated_data['email'],
          first_name=validated_data['first_name'],
          last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 



class LoginSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username','password', 'posts']
	
	
class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title','body','header_image','author')


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
	

    