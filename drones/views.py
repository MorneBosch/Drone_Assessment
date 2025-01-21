from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Drone, Medication
from .serializers import DroneSerializer, MedicationSerializer
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

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

# Register new Drone
@api_view(['POST'])
def register_drone(request):
    if request.method == 'POST':
        data = request.data
        serializer = DroneSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                "message": f"Drone {serializer.validated_data['serial_number']} registered successfully.",
                "drone": serializer.data
            }, status=201)
        return JsonResponse(serializer.errors, status=400)

# Load Medication onto drone
@csrf_exempt
def load_medication(request, pk):
    if request.method == 'POST':
        try:
            drone = Drone.objects.get(pk=pk)
            data = json.loads(request.body)
            medication_ids = data.get("medication_ids", [])

            # Validate input
            if not medication_ids:
                return JsonResponse({"error": "No medication IDs provided."}, status=400)

            try:
                medications = Medication.objects.filter(id__in=medication_ids)
                if medications.count() != len(medication_ids):
                    return JsonResponse({"error": "One or more Medications not found."}, status=404)
            except ValueError:
                return JsonResponse({"error": "Medication IDs must be valid integers."}, status=400)

            # Check if drone's battery is sufficient for loading
            if drone.battery_capacity < 25:
                return JsonResponse({"error": "Drone battery level must be above 25% to load medications."}, status=400)

            # Attempt to load medications and validate total weight
            try:
                drone.load_medication(medications)
                return JsonResponse({
                    "message": f"Medications successfully loaded onto drone {drone.serial_number}.",
                    "drone_state": drone.state,
                }, status=200)
            except ValidationError as e:
                return JsonResponse({"error": str(e)}, status=400)

        except Drone.DoesNotExist:
            return JsonResponse({"error": "Drone not found."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data provided."}, status=400)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)

# Retrieve medications loaded onto the drone
def get_loaded_medications(request, pk):
    # Check if the drone exists
    try:
        drone = Drone.objects.get(pk=pk)
    except Drone.DoesNotExist:
        return JsonResponse({"error": "Drone not found."}, status=404)

    # Retrieve medications
    medications = drone.medications.all()

    # If medications are found, return them as JSON
    if medications.exists():
        medications_data = [
            {
                'id': medication.id,
                'name': medication.name,
                'weight': medication.weight,
                'code': medication.code,
                'image': medication.image.url if medication.image else None
            }
            for medication in medications
        ]
        return JsonResponse(medications_data, safe=False)
    else:
        return JsonResponse({"message": "No medications loaded on this drone."}, status=404)

# Show available drones with battery status > 25%
def available_drones(request):
    # Filter drones with battery above 25% and state set to "IDLE"
    drones = Drone.objects.filter(battery_capacity__gt=25, state=Drone.IDLE)
    
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

# Send a drone to deliver
@csrf_exempt
def send_drone_to_deliver(request, pk):
    if request.method == 'POST':
        try:
            drone = Drone.objects.get(pk=pk)

            # Check if the drone is in the "LOADING" state
            if drone.state != Drone.LOADING:
                return JsonResponse({"error": "Drone must be in 'LOADING' state to start delivery."}, status=400)

            # Update the state to "DELIVERING"
            drone.state = Drone.DELIVERING
            drone.save()

            return JsonResponse({"message": f"Drone {drone.serial_number} is now delivering."}, status=200)

        except Drone.DoesNotExist:
            return JsonResponse({"error": "Drone not found"}, status=404)

    return JsonResponse({"error": "Invalid request method. Use POST."}, status=400)