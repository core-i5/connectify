# post_service/views.py

from rest_framework import viewsets, permissions
from .models import Discussion, Comment, Hashtag
from .serializers import DiscussionSerializer, CommentSerializer, HashtagSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_elasticsearch_dsl.search import Search
from .documents import DiscussionDocument

class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_view(self, request, pk=None):
        discussion = self.get_object()
        discussion.view_count += 1
        discussion.save()
        return Response(status=200)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', None)
        if query:
            s = Search(index='discussions').query('multi_match', query=query, fields=['text'])
            response = s.execute()
            results = [
                {
                    'id': hit.meta.id,
                    'text': hit.text,
                    'created_on': hit.created_on,
                    'user': {
                        'id': hit.user.id,
                        'username': hit.user.username
                    }
                }
                for hit in response
            ]
            return Response(results)
        return Response([])

    @action(detail=False, methods=['get'])
    def search_by_hashtag(self, request):
        hashtag = request.query_params.get('hashtag', None)
        if hashtag:
            discussions = Discussion.objects.filter(hashtags__name__icontains=hashtag)
            serializer = self.get_serializer(discussions, many=True)
            return Response(serializer.data)
        return Response([])

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        comment = self.get_object()
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        comment.save()
        return Response(status=200)

class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [permissions.IsAuthenticated]
