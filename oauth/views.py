from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from oauth.models import User, Friendship
from oauth.serializers import UserCreateSerializer, \
    FriendshipSerializer, UserListSendRequestSerializer, UserListReceiveRequestSerializer, \
    UserSerializer


@extend_schema(
    description="Создает нового пользователя. " \
                "Принимает имя пользователя и пароль.",
    summary="Авторизация пользователя"
)
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


@extend_schema(
    description="Отправляет запрос в друзья другому пользователю. " \
                "Принимает идентификатор получателя.",
    summary="Отправка заявки в друзья"
)
class SendFriendRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, to_user_id, *args, **kwargs):

        try:
            to_user = get_object_or_404(User, id=to_user_id)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        if to_user not in request.user.friends.all():
            if request.user == to_user:
                return Response({
                    "ERROR": "Вы не можете отправить запрос в друзья себе!"
                }, status=status.HTTP_400_BAD_REQUEST)

            elif Friendship.objects.filter(to_user=request.user, from_user=to_user).exists():
                request.user.friends.add(to_user)
                Friendship.objects.filter(to_user=request.user, from_user=to_user).delete()
                return Response({"detail": "Теперь вы друзья!"}, status=status.HTTP_200_OK)

            elif Friendship.objects.filter(to_user=to_user, from_user=request.user).exists():
                return Response({
                    "detail": "Вы уже отправили заявку в друзья этому пользователю!"
                }, status=status.HTTP_400_BAD_REQUEST)

            else:
                friend_request = Friendship.objects.create(to_user=to_user, from_user=request.user)
                serializer = FriendshipSerializer(friend_request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "detail": "Вы уже друзья!"
            }, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    description="Принимает запрос в друзья от другого пользователя. " \
                "Принимает идентификатор запроса.",
    summary="Прием заявки в друзья"
)
class AcceptFriendRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, from_user_id, *args, **kwargs):
        try:
            from_user = get_object_or_404(User, id=from_user_id)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        friendship = Friendship.objects.filter(to_user=request.user, from_user=from_user)
        if not friendship.exists():
            return Response({"detail": "Запрос в друзья не найден"}, status=status.HTTP_404_NOT_FOUND)
        request.user.friends.add(from_user)
        friendship.delete()
        return Response({"detail": "Теперь вы друзья!"}, status=status.HTTP_200_OK)


@extend_schema(
    description="Отклоняет запрос в друзья от другого пользователя. " \
                "Принимает идентификатор запроса.",
    summary="Отклонение запроса в друзья"
)
class RejectFriendRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, from_user_id, *args, **kwargs):
        try:
            from_user = get_object_or_404(User, id=from_user_id)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        friendship = Friendship.objects.filter(to_user=request.user, from_user=from_user)
        if not friendship.exists():
            return Response({"detail": "Запрос в друзья не найден"}, status=status.HTTP_404_NOT_FOUND)
        friendship.delete()
        return Response({"detail": "Запрос в друзья отклонен"}, status=status.HTTP_200_OK)


@extend_schema(
    description="Выводит информацию об исходящих заявках в друзья у данного пользователя: " \
                "id заявки и от какому пользователю был адресован запрос в друзья ",
    summary="Список исходящих заявок в друзья"
)
class ListSendFriendRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        friend_requests = Friendship.objects.filter(from_user=request.user)
        if not friend_requests.exists():
            return Response({"detail": "Исходящих заявок в друзья не найдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserListSendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    description="Выводит информацию о входящих заявках в друзья у данного пользователя: " \
                "id заявки и от какого пользователя пришел запрос на добавление в друзья ",
    summary="Список входящих заявок в друзья"
)
class ListReceiveFriendRequestView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        friend_requests = Friendship.objects.filter(to_user=request.user)
        if not friend_requests.exists():
            return Response({"detail": "Входящих заявок в друзья не найдено"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserListReceiveRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    description="Выводит информацию о статусе дружбы с пользователем, по его переданному id:",
    summary="Cтатус дружбы с пользователем"
)
class FriendshipStatusView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, other_user_id, *args, **kwargs):
        try:
            other_user = get_object_or_404(User, id=other_user_id)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        if other_user in request.user.friends.all():
            friendship_status = "Вы уже друзья"
        elif Friendship.objects.filter(from_user=request.user, to_user=other_user).exists():
            friendship_status = "У вас есть исходящая заявка в друзья этому пользователю"
        elif Friendship.objects.filter(from_user=other_user, to_user=request.user).exists():
            friendship_status = "У вас есть входящая заявка в друзья от этого пользователя"
        else:
            friendship_status = "Вы не друзья"
        return Response({"friendship_status": friendship_status}, status=status.HTTP_200_OK)

@extend_schema(
    description="Выводит информацию друзьях пользователя",
    summary="Список друзей"
)
class ListFriendsView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = request.user.friends.all()
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    description="Удаляет пользователя из друзей, по переданному id",
    summary="Удаление пользователя из друзей"
)
class DeleteFriendView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, other_user_id, *args, **kwargs):
        try:
            other_user = get_object_or_404(User, id=other_user_id)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)
        if other_user in request.user.friends.all():
            request.user.friends.remove(other_user)
            return Response({"detail": "Пользователь был удален из друзей"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Пользователь не был найден у вас в друзьях"}, status=status.HTTP_404_NOT_FOUND)
