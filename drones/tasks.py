import logging
from celery import shared_task
from .models import Drone, BatteryLog

# Configure logging
logger = logging.getLogger(__name__)

@shared_task
def log_battery_level():
    drones = Drone.objects.all()
    for drone in drones:
        # Log the battery capacity for the drone
        logger.info(f"Drone ID: {drone.id}, Battery Capacity: {drone.battery_capacity}%")

        # Create a BatteryLog entry for each drone
        BatteryLog.objects.create(
            drone=drone,
            battery_capacity=drone.battery_capacity,
        )

        # If the battery is too low, update the state to IDLE
        if drone.battery_capacity < 25:
            drone.state = Drone.IDLE
            drone.save()

    return f"Logged battery levels for {drones.count()} drones."