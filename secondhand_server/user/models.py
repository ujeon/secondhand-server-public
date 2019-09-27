from django.conf import settings
from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    nickname = models.CharField(max_length=10)
    password = models.CharField(max_length=255)
    third_party_token = models.CharField(max_length=255)
    signup_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email


class Favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filtered_data_id = models.IntegerField()

    def __str__(self):
        return self.filtered_data_id

