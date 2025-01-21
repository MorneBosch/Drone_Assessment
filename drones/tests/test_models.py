import os
import django

# Ensure Django settings are configured
os.environ['DJANGO_SETTINGS_MODULE'] = 'drone_assessment.settings'
django.setup()

from django.test import TestCase
from drones.models import Drone, Medication
from django.core.exceptions import ValidationError

class MedicationModelTest(TestCase):
    
    def setUp(self):
        """Set up a sample drone for testing."""
        self.drone = Drone.objects.create(
            serial_number="DRONE123",
            model="Lightweight",
            weight_limit=100,
            battery_capacity=50,
            state=Drone.IDLE,
        )

    def test_valid_medication_code(self):
        """Test that valid medication codes pass validation."""
        medication = Medication.objects.create(
            name="Test_Medication",
            weight=50.0,
            code="VALID_CODE_123",
        )
        self.assertEqual(medication.code, "VALID_CODE_123")

    def test_invalid_medication_code(self):
        """Test that invalid medication codes raise a ValidationError."""
        medication = Medication(
            name="Invalid_Med",
            weight=50.0,
            code="Invalid Code!"
        )
        with self.assertRaises(ValidationError):
            medication.full_clean()

    def test_load_medication_exceeds_weight_limit(self):
        """Test that loading medication exceeding the drone's weight limit raises a ValidationError."""
        medication1 = Medication.objects.create(name="Med1", weight=60.0, code="CODE_123")
        medication2 = Medication.objects.create(name="Med2", weight=50.0, code="CODE_456")

        # Loading the first medication
        self.drone.load_medication([medication1])
        with self.assertRaises(ValidationError):
            self.drone.load_medication([medication2])  # This should exceed the weight limit

class DroneModelTest(TestCase):
    def setUp(self):
        """Set up a sample drone for testing."""
        self.drone = Drone.objects.create(
            serial_number="DRONE123",
            model="Lightweight",
            weight_limit=100,
            battery_capacity=50,
            state=Drone.IDLE,
        )

    def test_update_state_below_25(self):
        """Test that a drone switches to IDLE if the battery drops below 25%."""
        self.drone.set_battery(20)
        self.assertEqual(self.drone.state, Drone.IDLE)