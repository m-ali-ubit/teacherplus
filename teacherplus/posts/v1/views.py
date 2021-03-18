from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet
from rest_framework import generics, mixins, views

from teacherplus.posts.models import Post, Activity, PostVote, Comment, CommentLike
from teacherplus.posts.v1.serializers import (
    ActivitySerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostVoteSerializer,
    CommentSerializer,
    CommentLikeSerializer,
)
from rest_framework.decorators import action
import logging

logger = logging.getLogger(__name__)


class ActivityView(GenericViewSet, ListModelMixin):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        return queryset


class PostView(ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostDetailSerializer

    def get_queryset(self):
        visited_user_id = self.request.query_params.get("visited_user_id")
        if visited_user_id:
            return Post.objects.filter(user=visited_user_id)
        return Post.objects.filter(user=self.request.user)


class PostVoteView(ViewSet):
    @action(methods=["POST"])
    def vote(self, request):
        try:
            post_vote_serializer = PostVoteSerializer(request.data)
            post_vote_serializer.is_valid(raise_exception=True)
            post_vote_serializer.save()
            return Response(data="Vote added.", status=status.HTTP_200_OK)
        except ValidationError as error:
            logger.error(f"Validation Error: {error}")
            return Response(
                data=error.default_detail, status=status.HTTP_400_BAD_REQUEST
            )


class CommentView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = CommentSerializer

    def get_queryset(self):
        visited_user_id = self.request.query_params.get("visited_user_id")
        if visited_user_id:
            return Post.objects.filter(user=visited_user_id)
        return Post.objects.filter(user=self.request.user)
