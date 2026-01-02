from django.db import models
from django.utils import timezone


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    market = models.ForeignKey(
        "market.Market", db_column="market_id", on_delete=models.DO_NOTHING, related_name="comments"
    )
    user = models.ForeignKey(
        "market.User", db_column="user_id", on_delete=models.DO_NOTHING, related_name="comments"
    )
    parent = models.ForeignKey(
        "self",
        db_column="parent_id",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="replies",
    )
    content = models.TextField()
    status = models.TextField(default="active")
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        "market.User",
        db_column="deleted_by",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="deleted_comments",
    )
    edited_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now)
    event = models.ForeignKey(
        "market.Event",
        db_column="event_id",
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="event_comments",
    )

    class Meta:
        managed = False
        db_table = "comments"

    def __str__(self) -> str:
        return f"{self.market_id}:{self.user_id}:{self.content[:20]}"


