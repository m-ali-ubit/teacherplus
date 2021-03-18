from django.db import models
from django.contrib import admin


class CreateUpdateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class ReadOnlyDateMixin(admin.ModelAdmin):
    readonly_fields = ("created_at", "last_updated_at")
