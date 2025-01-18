from django.db import models

class Drone(models.Model):
    serial_number = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight_limit = models.IntegerField()
    battery_capacity = models.IntegerField()
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.serial_number

class Medication(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    code = models.CharField(max_length=100)
    image = models.ImageField(upload_to='medications/')

    def __str__(self):
        return self.name