from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Drone, Medication
from .serializers import DroneSerializer, MedicationSerializer
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

# List of drones
@api_view(['GET'])
def drone_list(request):
    drones = Drone.objects.all()
    serializer = DroneSerializer(drones, many=True)
    return JsonResponse(serializer.data, safe=False)

# List of Medication
@api_view(['GET'])
def medication_list(request):
    if request.method == 'GET':
        medications = Medication.objects.all().values()
        return JsonResponse(list(medications), safe=False)

# Load medications onto a drone
@csrf_exempt
def load_medication(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        medication_ids = data.get("medication_ids", [])

        # Validate input
        if not medication_ids:
            return JsonResponse({"error": "No medication ID provided."}, status=400)

        try:
            medication_ids = [int(id) for id in medication_ids]  # Ensure IDs are integers
        except ValueError:
            return JsonResponse({"error": "Medication IDs must be integers."}, status=400)

        try:
            drone = Drone.objects.get(pk=pk)
            medications = Medication.objects.filter(id__in=medication_ids)

            # Check medication existence or weight limit
            if medications.count() != len(medication_ids):
                return JsonResponse({"error": "One or more Medications not found."}, status=404)

            # Check total weight of medications against drone's weight limit
            total_weight = sum([med.weight for med in medications])
            if total_weight > drone.weight_limit:
                return JsonResponse({"error": "Total weight of medications exceeds the drone's weight limit."}, status=400)

            # Load medications onto the drone
            drone.state = 'Loaded with medications'
            drone.medications.set(medications)
            drone.save()

            return JsonResponse({"message": f"Drone {drone.serial_number} loaded with medications."}, status=200)

        except Drone.DoesNotExist:
            return JsonResponse({"error": "Drone not found"}, status=404)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

# Retrieve medications loaded onto the drone
def get_loaded_medications(request, pk):
    drone = get_object_or_404(Drone, pk=pk)

    # Retrieve medications
    medications = drone.medications.all()

    # If medications are found, return them as JSON
    if medications:
        medications_data = [{
            'id': medication.id,
            'name': medication.name,
            'weight': medication.weight,
            'code': medication.code,
            'image': medication.image.url if medication.image else None
        } for medication in medications]

        return JsonResponse(medications_data, safe=False)
    else:
        return JsonResponse({"message": "No medications loaded on this drone."}, status=404)
    
# Show available drones with battery status > 25%
def available_drones(request):
    # Filter drones with battery above 25% and state set to "Available"
    drones = Drone.objects.filter(battery_capacity__gt=25, state="Available")
    
    if drones.exists():
        drone_data = []
        for drone in drones:
            drone_data.append({
                "id": drone.id,
                "serial_number": drone.serial_number,
                "model": drone.model,
                "weight_limit": drone.weight_limit,
                "battery_capacity": drone.battery_capacity,
                "state": drone.state
            })
        return JsonResponse({"available_drones": drone_data}, status=200)
    else:
        return JsonResponse({"message": "No available drones found with more than 25% battery."}, status=404)
    
# Get battery status of specified drone
def get_battery_level(request, pk):
    try:
        drone = Drone.objects.get(pk=pk)
        return JsonResponse({"drone_id": drone.pk, "battery_capacity": drone.battery_capacity}, status=200)
    except Drone.DoesNotExist:
        return JsonResponse({"error": "Drone not found."}, status=404)