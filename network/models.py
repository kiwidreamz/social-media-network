from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	dateandtime = models.DateTimeField()
	text = models.TextField(max_length=560)
	likes = models.PositiveIntegerField(default=0)

class Following(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	following = models.ForeignKey(User, related_name='isfollowing', on_delete=models.DO_NOTHING,)

class Likez(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Posts, on_delete=models.CASCADE)
