from rest_framework import serializers

from teacherplus.posts.models import Activity, Post, PostVote, Comment, CommentLike


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        exclude = ("last_updated_at",)


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("votes",)


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "author",
            "title",
            "created_at",
            "last_updated_at",
            # "up_vote_count",
            # "down_vote_count",
        )


class PostVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVote


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"
