import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import slugify

from teacherplus.mixins import CreateUpdateMixin

User = get_user_model()

VOTE_CHOICES = [("up_vote", "Up Vote"), ("down_vote", "Down Vote")]
ACTIVITY_TYPES = VOTE_CHOICES + [("like", "Like")]


class Activity(CreateUpdateMixin):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "Activities"


class Post(CreateUpdateMixin):

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    post_text = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    votes = GenericRelation(Activity)

    # up_vote_count = models.IntegerField(default=0)
    # down_vote_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["created_at"]


class PostVote(CreateUpdateMixin):

    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(max_length=10, choices=VOTE_CHOICES)

    def __str__(self):
        return f"{self.user}|{self.post}|{self.vote}"

    class Meta:
        unique_together = ("user", "post", "vote")
        ordering = ["created_at"]


class Comment(CreateUpdateMixin):

    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    slug = models.SlugField(unique=True, default=uuid.uuid4)
    likes = GenericRelation(Activity)
    # likes_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.text)[:20]

    class Meta:
        ordering = ["created_at"]


class CommentLike(CreateUpdateMixin):

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "comment")
        ordering = ["created_at"]
