from django.db import models
from devtools.models import Devtool

# Create your models here.
class Idea(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='idea_imgs', blank=True, null=True)
    content = models.TextField(blank=True)
    interest = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    devtool = models.ForeignKey(
        Devtool,
        on_delete=models.CASCADE,
        related_name='ideas'
    )

    def __str__(self):
        return self.title

class IdeaStar(models.Model):
    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        related_name='stars'
    )
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('idea', 'session_key')

    def __str__(self):
        return f"{self.idea.title} - {self.session_key}"