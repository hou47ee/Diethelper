from django.db import models
from django.contrib.auth.models import User

class Bodydata(models.Model):
    member = models.ForeignKey(User,on_delete=models.CASCADE,db_column='member')
    height = models.FloatField()
    weight = models.FloatField()
    BMI = models.FloatField()
    time = models.DateTimeField(primary_key=True)
    