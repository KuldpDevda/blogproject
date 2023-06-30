from django.urls import path,include
from api_view.views import ChangePasswordView,RegisterUserAPIView,PostAPIView, PostDetailAPIView , PostUpdateAPI ,UpdateAPI,PostCreateAPI,DeleteProfileAPI, UserLoginAPI,LogoutAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import DefaultRouter
from api_view.views import PostViewSet ,UserViewSet
from rest_framework.authtoken.views import obtain_auth_token  



schema_view = get_schema_view(
   openapi.Info(
      title="blogProject API",
      default_version='v1',
      description="User description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@xyz.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

def trigger_error(request):
    division_by_zero = 1 / 0

router = DefaultRouter()
router.register('post', PostViewSet,basename="post")
router.register('users', UserViewSet,basename="users")


urlpatterns = [
   path('post/', PostAPIView.as_view()),
   path('create/',PostCreateAPI.as_view()),
	path('<int:pk>/', PostDetailAPIView.as_view()),
   path('register/',RegisterUserAPIView.as_view()),
   path('login/',UserLoginAPI.as_view()),
   path('logout/',LogoutAPIView.as_view()),
   path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
   path('change-password/', ChangePasswordView.as_view()),
   path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
 #    path('update/<int:pk>/',UpdateAPI.as_view()),
 #    path('delete/',DeleteProfileAPI.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('sentry/', trigger_error),
    path('', include(router.urls)),


    # path('postupdate',PostUpdateAPI.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
    # path('api/v1/rest-auth/', include('rest_auth.urls'))
    # path('', views.send_mail, name='sendmail'),
    # path('<int:pk>/update/',PostAPIUpdate.as_view()),
    # path('<int:pk>/dalete/',PostAPIDelete.as_view()),
]