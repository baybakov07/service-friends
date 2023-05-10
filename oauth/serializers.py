from rest_framework import serializers

from oauth.models import User, Friendship


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = '__all__'

class UserListSendRequestSerializer(serializers.ModelSerializer):
    to_user = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ('id', 'to_user')

class UserListReceiveRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ('id', 'from_user')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']