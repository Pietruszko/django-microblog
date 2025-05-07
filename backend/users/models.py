from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class UserProfile(models.Model):
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    bio = models.TextField(default="This is my profile!", blank=True)
    avatar = CloudinaryField('image', default='default-avatar_rwky8f')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
