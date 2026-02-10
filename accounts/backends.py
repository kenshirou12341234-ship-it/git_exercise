from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


User = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
           return None
        
        except User.MultipleObjectsReturned:
           return None
        
        if user.check_password(password):
            return user 

        else :
            return None