from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatHistory(models.Model):
    TASK_CHOICES = (
        ("summarize", "Summarize"),
        ("sentiment", "Sentiment"),
        ("generate", "Generate"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=20, choices=TASK_CHOICES)
    input_text = models.TextField()
    result_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.task}"
