from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class ModelBackendCustom(ModelBackend):
    def authenticate(self, request, login=None, password=None, **kwargs):
        if login and password:
            try:
                user = UserModel._default_manager.get_by_natural_key(login)
            except UserModel.DoesNotExist:
                UserModel().set_password(password)
            else:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
