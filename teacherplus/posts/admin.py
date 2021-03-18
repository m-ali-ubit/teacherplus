from django.contrib import admin

from teacherplus.mixins import ReadOnlyDateMixin
from teacherplus.posts.models import Post, Activity, PostVote, Comment, CommentLike


class ActivityAdmin(ReadOnlyDateMixin):
    list_display = ["id", "user", "activity_type", "content_type"]


class PostAdmin(ReadOnlyDateMixin):
    list_display = ["id", "author", "title"]


class PostVoteAdmin(ReadOnlyDateMixin):
    list_display = ["id", "post", "user", "vote"]


class CommentAdmin(ReadOnlyDateMixin):
    list_display = ["id", "post", "author"]


class CommentLikeAdmin(ReadOnlyDateMixin):
    list_display = ["id", "comment", "user"]


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostVote, PostVoteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
