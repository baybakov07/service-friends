from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    def __str__(self):
        return self.username


class Friendship(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incoming_friend_requests')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outgoing_friend_requests')

    def __str__(self):
        return f'{self.from_user} sent a friendship request to {self.to_user}'
