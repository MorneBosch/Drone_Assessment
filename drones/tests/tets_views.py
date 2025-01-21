import os
import django

# Ensure Django settings are configured
os.environ['DJANGO_SETTINGS_MODULE'] = 'drone_assessment.settings'
django.setup()

from django.test import TestCase
from django.urls import reverse
from drones.models import Drone, Medication

class MedicationListViewTest(TestCase):
    def setUp(self):
        self.medication1 = Medication.objects.create(name="Med1", weight=20.0, code="CODE1")
        self.medication2 = Medication.objects.create(name="Med2", weight=30.0, code="CODE2")

    def test_medication_list(self):
        """Test retrieving the list of medications."""
        response = self.client.get(reverse('medication_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Med1')

class LoadMedicationViewTest(TestCase):
    def setUp(self):
        self.drone = Drone.objects.create(
            serial_number="DRONE123",
            model="Lightweight",
            weight_limit=100,
            battery_capacity=50,
            state=Drone.IDLE,
        )
        self.medication1 = Medication.objects.create(name="Med1", weight=20.0, code="CODE1")
        self.medication2 = Medication.objects.create(name="Med2", weight=30.0, code="CODE2")

    def test_load_medication_success(self):
        """Test successful loading of medication onto a drone."""
        response = self.client.post(
            reverse('load_medication', kwargs={'pk': self.drone.id}),
            data={"medication_ids": [self.medication1.id, self.medication2.id]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.drone.refresh_from_db()
        self.assertEqual(self.drone.medications.count(), 2)
        self.assertEqual(self.drone.state, Drone.LOADING)

    def test_load_medication_exceeds_weight(self):
        """Test that loading fails when medication weight exceeds drone limit."""
        self.drone.weight_limit = 30  # Reduce weight limit
        self.drone.save()

        response = self.client.post(
            reverse('load_medication', kwargs={'pk': self.drone.id}),
            data={"medication_ids": [self.medication1.id, self.medication2.id]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_load_medication_battery_too_low(self):
        """Test that loading fails when battery is below 25%."""
        self.drone.battery_capacity = 20
        self.drone.save()

        response = self.client.post(
            reverse('load_medication', kwargs={'pk': self.drone.id}),
            data={"medication_ids": [self.medication1.id]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())