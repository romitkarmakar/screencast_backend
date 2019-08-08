from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=200,blank=True)
    email = models.CharField(max_length=200)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.name