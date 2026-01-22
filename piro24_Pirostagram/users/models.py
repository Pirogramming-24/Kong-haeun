from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    image = models.ImageField(
        upload_to='profils/',
        default='profiles/default.png',
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username

class Follow(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.from_user} → {self.to_user}'
