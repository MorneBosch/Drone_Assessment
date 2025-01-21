# Drone Fleet Management System

## Project Overview
The Drone Fleet Management System is a service designed to manage a fleet of drones for delivering medication. It supports tasks such as loading medications onto drones, monitoring battery levels, and managing drone states. The system includes a REST API for interacting with the drones and a periodic task for logging battery history.

## Requirements

### Software Requirements
- Python 3.9 or higher
- Django 4.x
- Celery 5.x
- Redis (as a message broker for Celery)

### Python Dependencies
All required dependencies are listed in `requirements.txt`. Install them using the following command:

```bash
pip install -r requirements.txt
```

## Setup Instructions

### 1. Clone the Repository
Clone the project repository to your local machine:

```bash
git clone https://github.com/MorneBosch/Drone_Assessment.git
cd Drone_Assessment
```
### Set Up a Virtual Environment
Create and activate a virtual environment:

```bash
python -m venv venv
source venv\Scripts\activate   # For Windows
```

### Install Dependencies
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure the Database
Update the `DATABASES` settings in `settings.py` to match your database configuration. By default, SQLite is used.

### 5. Apply Migrations
Set up the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Load Preloaded Data
Load sample data into the database to initialize the application with default drone and medication information:

```bash
python manage.py loaddata preloaded_data.json
```

### 7. Start the Django Server
Run the development server:

```bash
python manage.py runserver
```

### 8. Start the Celery Worker
Start the Celery worker to handle background tasks:

```bash
celery -A drones worker --loglevel=info
```

### 9. Start the Celery Beat Scheduler
To schedule periodic tasks:

```bash
celery -A drones beat --loglevel=info
```

## API Endpoints

### Drone Endpoints
- **GET /drones/**: List all drones.
- **POST /drones/**: Register a new drone.
- **PATCH /drones/<id>/**: Update a drone's details.
- **POST /drones/<id>/send_to_deliver/**: Send a drone to deliver loaded medication.

### Medication Endpoints
- **GET /medications/**: List all medications.
- **POST /medications/**: Add a new medication.

### Load Medications
- **POST /drones/<id>/load/**: Load medications onto a specified drone.

### Battery and State Checks
- **GET /drones/<id>/battery/**: Check the battery level of a specific drone.
- **GET /drones/available/**: List all available drones for loading (battery > 25%, state is IDLE).

## Testing

### Running Tests
To run tests for the application:

```bash
python manage.py test
```

### Suggested Tests

#### Model Tests
- Validate constraints and behaviors of models (e.g., Drone, Medication).

#### View Tests
- Test API endpoints for valid and invalid inputs.

#### Periodic Tasks
The system includes a periodic task to:

- Monitor drone battery levels.
- Log battery history into the `BatteryLog` table.
- Ensure Celery and Redis are properly configured to enable periodic tasks.