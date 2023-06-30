from rest_framework import generics,permissions,status,viewsets
from blog.models import Post
from blog.serializer import RegisterSerializer,PostSerializer, LoginSerializer, UserProfileSerializer,UserSerializer,ChangePasswordSerializer
from django.core.mail import send_mail,EmailMessage
from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.contrib.auth.models import User
from django.template import Context
from django.template.loader import render_to_string, get_template
from rest_framework.response import Response
from django.contrib.auth import login, authenticate,logout
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
# from rest_framework.status import (
#     HTTP_400_BAD_REQUEST,
#     HTTP_404_NOT_FOUND,
#     HTTP_200_OK
# )


from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
# from blog.logs import exception,logger
from rest_framework import generics
from django.utils import timezone
import pytz
import datetime

class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    # @exception(logger)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "Message":"You are Successfully Registered"}, status=status.HTTP_200_OK)
        else:
            return Response({"Message":[serializer.errors]}, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated,]

    # @exception(logger)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class UserLoginAPI(generics.CreateAPIView):
    serializer_class = LoginSerializer
    queryset = User.objects.all()

    # @exception(logger)
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)

        utc_now = timezone.now()
        utc_now = utc_now.replace(tzinfo = pytz.utc)
        token = Token.objects.filter(user=user, created__lt = utc_now - datetime.timedelta(seconds=30)).delete()
        token,create = Token.objects.get_or_create(user=user)
        token.save()
        token = str(token)
        data={
                "token":token,
                "username":username,
                }
        return Response({'data':data},status=status.HTTP_200_OK)


class LogoutAPIView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response({"message": "logout successfully", 'code': status.HTTP_200_OK,}) 


class UpdateAPI(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DeleteProfileAPI(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        user=self.request.user
        user.delete()

        return Response({"result":"user delete"})


class PostCreateAPI(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.user.id)
        user_email = user.email
        merge_data = {
            'greetings': "Hello"
         }
        html_message = get_template('blog/message.html').render(merge_data)
        from_email = settings.EMAIL_HOST_USER
        msg = EmailMessage('Hey Kuldeep !',
                   html_message,
                   from_email,
                  [user_email],
                 )
        msg.content_subtype ="html"
        msg.send()
        print("Mail successfully sent")

    
class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostUpdateAPI(generics.UpdateAPIView):
    queryset = Post.objects.filter()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
