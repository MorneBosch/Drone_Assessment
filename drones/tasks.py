from celery import shared_task
from .models import Drone, BatteryLog

@shared_task
def check_battery_levels():
    drones = Drone.objects.all()
    for drone in drones:
        # Create a BatteryLog entry for each drone
        BatteryLog.objects.create(
            drone=drone,
            battery_capacity=drone.battery_capacity,
        )
        # If the battery is too low, update the state to IDLE
        if drone.battery_capacity < 25:
            drone.state = Drone.IDLE
            drone.save()
