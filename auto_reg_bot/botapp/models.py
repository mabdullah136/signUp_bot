from django.db import models

class BotJob(models.Model):
    target_url = models.URLField()
    username_prefix = models.CharField(max_length=50)
    limit = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"{self.username_prefix} ({self.limit})"