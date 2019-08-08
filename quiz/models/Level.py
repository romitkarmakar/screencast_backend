from django.db import models

class Level(models.Model):
    level_number = models.IntegerField(default=1)
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    end_time = models.DateTimeField(auto_now_add=True, blank=True)
