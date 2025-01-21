from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Drone(models.Model):
    # Define states as constants
    IDLE = 'IDLE'
    LOADING = 'LOADING'
    LOADED = 'LOADED'
    DELIVERING = 'DELIVERING'
    DELIVERED = 'DELIVERED'
    RETURNING = 'RETURNING'

    STATE_CHOICES = [
        (IDLE, 'IDLE'),
        (LOADING, 'LOADING'),
        (LOADED, 'LOADED'),
        (DELIVERING, 'DELIVERING'),
        (DELIVERED, 'DELIVERED'),
        (RETURNING, 'RETURNING'),
    ]

    # Enum-like choices for model type
    MODEL_CHOICES = [
        ('Lightweight', 'Lightweight'),
        ('Middleweight', 'Middleweight'),
        ('Cruiserweight', 'Cruiserweight'),
        ('Heavyweight', 'Heavyweight'),
    ]

    serial_number = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100, choices=MODEL_CHOICES)
    weight_limit = models.IntegerField()
    battery_capacity = models.IntegerField()
    state = models.CharField(max_length=100, choices=STATE_CHOICES, default=IDLE)
    medications = models.ManyToManyField('Medication', related_name="drones", blank=True)

    def __str__(self):
        return self.serial_number

    def validate_loading(self):
        """Ensure the drone can be set to LOADING state."""
        if self.battery_capacity < 25:
            raise ValidationError("Battery must be greater than 25% to load medications.")
    
    def load_medication(self, medications):
        """Load medications onto the drone and validate weight."""
        # Total weight validation
        total_weight = sum(med.weight for med in medications) + sum(med.weight for med in self.medications.all())
        if total_weight > self.weight_limit:
            raise ValidationError("Total weight exceeds the drone's weight limit.")

        self.medications.add(*medications)
        if self.state == self.IDLE:
            self.state = self.LOADING
        self.save()

    def update_state(self):
        """Update the state based on battery level or other conditions."""
        if self.battery_capacity < 25:
            self.state = self.IDLE  # Set to IDLE if battery is below 25%
        self.save()

    def set_battery(self, new_battery_capacity):
        """Update battery capacity and validate state."""
        self.battery_capacity = new_battery_capacity
        self.update_state()
        self.save()

class Medication(models.Model):
    CODE_VALIDATOR = RegexValidator(
        regex=r'^[A-Z0-9_]+$',
        message="Code must contain only uppercase letters, numbers, and underscores."
    )

    name = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9-_]+$',
                message="Name can only contain letters, numbers, dashes, and underscores."
            )
        ]
    )
    weight = models.FloatField()
    code = models.CharField(max_length=255, validators=[CODE_VALIDATOR])
    image = models.ImageField(upload_to='medication_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class BatteryLog(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name="battery_logs")
    timestamp = models.DateTimeField(auto_now_add=True)
    battery_capacity = models.IntegerField()

    def __str__(self):
        return f"{self.drone.serial_number} - {self.battery_capacity}% @ {self.timestamp}"
