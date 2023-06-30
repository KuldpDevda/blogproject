from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings



class Post(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    header_image = models.ImageField(null=True, blank=True,upload_to="post_detail")
    author = models.ForeignKey('auth.User',related_name='posts',on_delete=models.CASCADE,)                                    
    body = models.TextField()
    likes = models.ManyToManyField(User,related_name="like",blank=True,default=None)
   
    def total_likes(self):
        return self.likes.all().count()
        
    def __str__(self):
        return self.title  

 
    def get_absolute_url(self):
        return reverse('blog:post_detail',args=[str(self.id)])

    @property
    def number_of_comments(self):
        return Comment.objects.filter(blogpost_connected=self).count()


    class Meta:
        ordering = ['-date']
   

class Comment(models.Model):
    author = models.ForeignKey('auth.User',on_delete=models.CASCADE,)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.content

    

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
