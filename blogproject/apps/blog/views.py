from django.views.generic import ListView, DetailView , View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from .models import Post,Comment
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from .forms import CommentForm,UserRegisterForm, ProfileUpdateForm,EmailForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework import generics
from django.core.mail import send_mail
# from rest_framework.authtoken.views import ObtainAuthToken


# def token(request):
#     return render(request,"token.html", {'token_apikey': settings.TOKEN_APIKEY, 'environment': settings.ENVIRONMENT})

# def genrate_token(request):
#     endpoint = f"{settings.BASE_URL}get_auth_token"
#     data = {"username": "admin009", "password": "asdf@123"}
#     response = requests.request("POST", endpoint, data=data).json()
#     return JsonResponse(response)


# class CustomObtainAuthToken(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
#         token = Token.objects.get(key=response.data['token'])
#         league_id = UserProfile.objects.get(pk=token.user_id)
#         user = UserProfile.objects.get(pk=token.user_id)
#         return Response({'token': token.key, 'user_id': token.user_id, 'first_name': user.first_name, 'last_name': user.last_name,})


class ProfileUpdateView(UpdateView):
    form_class = ProfileUpdateForm
    queryset = User.objects.all()
    template_name = 'blog/profile_edit.html'
    success_url = reverse_lazy('blog:profile')


class ProfileView(ListView):
    model = Post
    template_name='blog/profile.html'

    def get_queryset(self):
        author_id = self.request.user
        return Post.objects.filter(author=author_id).order_by("date")


class SignUpView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'blog/signup.html'


class BlogListView(ListView):
    model = Post
    template_name = 'home.html'
    


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


    
def add_comment(request, *args, **kwargs):
        objs = Post.objects.filter(id=kwargs['pk'])[0]
        obj = objs.comment_set.create(author=request.user, content=request.POST.get('content'))
        response = {
            'user': obj.author.username,
            'content': obj.content,
            'post': obj.post.id,
            'created': obj.created,
            'count': objs.comment_set.count()
        }
        return JsonResponse(response)


class BlogCreateView(CreateView,LoginRequiredMixin):
    model = Post
    template_name = 'blog/post_new.html'
    fields = ['title','header_image','body']
    

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title','header_image', 'body']


class BlogDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("blog:home")
    template_name = 'blog/post_delete.html'
    
    
class BlogImage(ListView):
    model = Post
    template_name = 'blog/post_detail.html'


@login_required
def like_post(request,pk): 
    if request.method == "POST":
        post = get_object_or_404(Post,id=request.POST.get('post_id',pk))
        id=pk
        is_liked=False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user.id)
            is_liked=False
        else:
            post.likes.add(request.user.id)
            is_liked=True            

        total_dict={'total_likes':post.total_likes(),'is_liked':is_liked}

        return JsonResponse(total_dict)

def sendMail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = "Sending an for successful Regitering to our site"
            message = "Wel COme to our website you are a Successfully user for our site Enjoy."
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, [cd['recipient']])
    return render(request, 'homepage.html')



    