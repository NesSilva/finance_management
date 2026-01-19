from django.db import models

class User(models.Model):
    id_user = models.AutoField(primary_key=True , unique=True , auto_created=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
