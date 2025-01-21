from django.urls import path
from . import views

urlpatterns = [
    path('', views.drone_list, name='drone_list'),  # Drone list
    path('medications/', views.medication_list, name='medication_list'),  # Medication list
    path('register/', views.register_drone, name='register_drone'), # Add new drone
    path('<int:pk>/load/', views.load_medication, name='load_medication'),  # Loading medication
    path('<int:pk>/medications/', views.get_loaded_medications, name='get_loaded_medications'),  # Check loaded Medication
    path('available/', views.available_drones, name='available_drones'),  # Show available drones
    path('<int:pk>/battery/', views.get_battery_level, name='get_battery_level'),  # Check battery status
    path('<int:pk>/send-to-deliver/', views.send_drone_to_deliver, name='send_drone_to_deliver'),  # Send drone for delivery
]