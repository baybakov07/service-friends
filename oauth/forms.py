from django.contrib.auth.forms import UserChangeForm

from oauth.models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'