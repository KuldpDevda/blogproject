import datetime
import pytz
from django.conf import settings
# from django.utils import timezone
from rest_framework.authentication import TokenAuthentication,get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class ExpiringTokenAuthentication(TokenAuthentication):


    def authenticate_credentials(self, key, request=None):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed(
                {"error": "Invalid or Inactive Token", "is_authenticated": False}
            )

        if not token.user.is_active:
            raise AuthenticationFailed(
                {"error": "Invalid user", "is_authenticated": False}
            )

        utc_now = timezone.now()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - datetime.timedelta(seconds=30)
            raise AuthenticationFailed(
                {"error": "Token has expired", "is_authenticated": False}
            )
        return token.user, token