from django.db import models
from django.utils import timezone

class Drone(models.Model):
    serial_number = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    weight_limit = models.IntegerField()
    battery_capacity = models.IntegerField()
    state = models.CharField(max_length=100)
    medications = models.ManyToManyField('Medication', related_name="drones", blank=True)

    def __str__(self):
        return self.serial_number

class Medication(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    code = models.CharField(max_length=100)
    image = models.ImageField(upload_to='medications/')

    def __str__(self):
        return self.name
    
class BatteryLog(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    battery_capacity = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Drone {self.drone.serial_number} - {self.battery_capacity}% at {self.timestamp}"