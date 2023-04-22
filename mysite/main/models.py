from django.db import models

# Create your models here.

class MyUser(models.Model):
    
    name = models.CharField('User name', max_length=100)
    password = models.CharField('User password', max_length=100)

    def __str__(self):
        return self.name