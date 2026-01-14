from django.db import models

# Create your models here.
from django.db import models

class Vote(models.Model):
    choice = models.CharField(max_length=50)

    def __str__(self):
        return self.choice
