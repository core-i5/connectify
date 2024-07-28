from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, FollowSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user = self.get_object()
        if user.followers.filter(pk=request.user.pk).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.followers.add(request.user)
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user = self.get_object()
        if not user.followers.filter(pk=request.user.pk).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user.followers.remove(request.user)
        user.save()
        return Response(status=status.HTTP_200_OK)