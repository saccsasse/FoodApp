from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #when the User is deleted, their profile will also gonna be deleted ]
    image = models.ImageField(default='default_pic.jpg', upload_to='profile_pics')
    location = models.CharField(max_length=120)

    def __str__(self):
        return self.user.username


