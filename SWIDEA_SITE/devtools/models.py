from django.db import models

# Create your models here.
class Devtool(models.Model):
    name = models.CharField(max_length=30, unique=True)
    kind = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name