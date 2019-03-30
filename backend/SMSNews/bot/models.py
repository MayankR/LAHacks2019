from django.db import models

# Create your models here.

class UserInfo(models.Model):
	number = models.CharField(max_length=15)
	country = models.CharField(max_length=5)
	name = models.CharField(max_length=200)
	topic_idx = models.IntegerField(default=0)

	def __str__(self):
		return self.number