import os
import django

# Ensure Django settings are configured
os.environ['DJANGO_SETTINGS_MODULE'] = 'drone_assessment.settings'
django.setup()

from django.test import TestCase
from drones.models import Drone, BatteryLog
from drones.tasks import log_battery_level

class BatteryLogTaskTest(TestCase):
    def setUp(self):
        self.drone = Drone.objects.create(
            serial_number="DRONE123",
            model="Lightweight",
            weight_limit=100,
            battery_capacity=50,
            state=Drone.IDLE,
        )

    def test_check_battery_levels_creates_log(self):
        """Test that the periodic battery check logs the battery level."""
        log_battery_level()  # Manually invoke the task
        log_entry = BatteryLog.objects.filter(drone=self.drone).first()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry.battery_capacity, 50)

    def test_battery_drops_below_25(self):
        """Test that the drone state changes when the battery drops below 25%."""
        self.drone.battery_capacity = 20
        self.drone.save()

        log_battery_level()  # Manually invoke the task
        self.drone.refresh_from_db()
        self.assertEqual(self.drone.state, Drone.IDLE)
