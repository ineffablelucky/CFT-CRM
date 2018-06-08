from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            myuser = get_user_model()

            user = myuser.objects.get(email=username)
        except myuser.MultipleObjectsReturned:
            user = myuser.objects.filter(email=username).order_by('id').first()

        except myuser.DoesNotExist:
            return None

        if getattr(user, 'is_active') and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            myuser = get_user_model()
            return myuser.objects.get(pk=user_id)
        except myuser.DoesNotExist:
            return None