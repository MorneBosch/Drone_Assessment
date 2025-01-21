from rest_framework import serializers
from .models import Drone, Medication

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

class DroneRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ['serial_number', 'model', 'weight_limit', 'battery_capacity']

    def validate(self, data):
        if data['battery_capacity'] < 0 or data['battery_capacity'] > 100:
            raise serializers.ValidationError("Battery capacity must be between 0 and 100.")
        if data['weight_limit'] <= 0:
            raise serializers.ValidationError("Weight limit must be greater than 0.")
        return data