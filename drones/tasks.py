# drones/tasks.py
from celery import shared_task
from .models import Drone

@shared_task
def log_battery_level():
    # Retrieve all drones and log their battery levels
    drones = Drone.objects.all()
    battery_log = []
    
    for drone in drones:
        battery_log.append({
            'drone_id': drone.id,
            'serial_number': drone.serial_number,
            'battery_capacity': drone.battery_capacity
        })    
    return battery_log