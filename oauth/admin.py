from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from oauth.forms import CustomUserChangeForm
from oauth.models import User, Friendship


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm


admin.site.register(User, CustomUserAdmin)


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change and obj.to_user in obj.from_user.friends.all():
            return
        if Friendship.objects.filter(to_user=obj.from_user, from_user=obj.to_user).exists():
            Friendship.objects.filter(to_user=obj.from_user, from_user=obj.to_user).delete()
            obj.from_user.friends.add(obj.to_user)
            obj.to_user.friends.add(obj.from_user)
        else:
            obj.save()
