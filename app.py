from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
import heapq  # For priority queue
from datetime import datetime, timedelta  # To handle time slots and current time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management
socketio = SocketIO(app)

# Data storage
patients = {}  # Stores patient details
priority_queue = []  # Priority queue (min-heap) to manage patients
patient_counter = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["POST"])
def register():
    global patient_counter
    data = request.json
    patient_counter += 1
    patients[patient_counter] = {
        "name": data["name"],
        "age": data["age"],
        "contact": data["contact"],
        "address": data["address"],
        "time_slot": data["time_slot"],
        "priority": 3,  # Default priority (low)
        "description": "",
        "queue_number": None
    }
    print(patients)  # Print the updated patients dictionary

    # Emit a queue update to all clients
    queue_for_emit = [(priority, time_slot.strftime("%H:%M"), patient_id) for priority, time_slot, patient_id in priority_queue]
    socketio.emit('queue_update', {'queue': queue_for_emit, 'patients': patients})

    return jsonify({"success": True, "patient_id": patient_counter})


@app.route('/symptoms/<int:patient_id>')
def symptoms(patient_id):
    return render_template('symptoms.html', patient_id=patient_id)

@app.route('/add_symptoms', methods=["POST"])
def add_symptoms():
    data = request.json
    patient_id = int(data["patient_id"])  # Convert patient_id to integer
    patients[patient_id]["description"] = data["illness"]
    patients[patient_id]["priority"] = int(data["urgency"])

    # Add patient to the priority queue
    heapq.heappush(priority_queue, (
        patients[patient_id]["priority"],
        datetime.strptime(patients[patient_id]["time_slot"], "%H:%M"),  # Convert time_slot to datetime for comparison
        patient_id
    ))
    update_queue_numbers()

    # Convert datetime objects to strings before emitting
    queue_for_emit = [(priority, time_slot.strftime("%H:%M"), patient_id) for priority, time_slot, patient_id in priority_queue]

    # Notify all clients (patients and doctor) about the updated queue
    socketio.emit('queue_update', {'queue': queue_for_emit, 'patients': patients})

    # Redirect to the queue page
    return jsonify({
        "success": True,
        "redirect_url": url_for('queue', patient_id=patient_id)
    })

@app.route('/queue/<int:patient_id>')
def queue(patient_id):
    queue_number = patients[patient_id]["queue_number"]
    patients_ahead = len([p for p in priority_queue if patients[p[2]]["priority"] < patients[patient_id]["priority"]])
    return render_template('queue.html', queue_number=queue_number, patients_ahead=patients_ahead, patient_id=patient_id, patients=patients)
@app.route('/doctor')
def doctor():
    # Get the current time
    current_time = datetime.now().time()

    # Filter patients whose time slot is within ±1 hour of the current time
    filtered_patients = []
    for priority, time_slot, patient_id in priority_queue:
        time_slot_time = time_slot.time()
        time_difference = (datetime.combine(datetime.today(), time_slot_time) - datetime.combine(datetime.today(), current_time)).total_seconds() / 3600

        # If the time slot has passed or is within ±1 hour, include the patient
        if time_difference <= 1:  # ±1 hour window
            filtered_patients.append((priority, time_slot, patient_id))

    # Sort filtered patients by time slot (earlier first) and priority (higher first)
    sorted_patients = sorted(filtered_patients, key=lambda x: (x[1], x[0]))

    return render_template('doctor.html', patients=patients, queue=sorted_patients, current_time=current_time.strftime("%H:%M"))

@app.route('/close_patient', methods=["POST"])
def close_patient():
    patient_id = request.json["patient_id"]
    if patient_id in [p[2] for p in priority_queue]:
        priority_queue[:] = [p for p in priority_queue if p[2] != patient_id]
        update_queue_numbers()

        # Convert datetime objects to strings before emitting
        queue_for_emit = [(priority, time_slot.strftime("%H:%M"), patient_id) for priority, time_slot, patient_id in priority_queue]

        # Notify all clients (patients and doctor) about the updated queue
        socketio.emit('queue_update', {'queue': queue_for_emit, 'patients': patients})
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Patient not found in queue"})

def update_queue_numbers():
    """Update queue numbers based on priority and time slot."""
    sorted_queue = sorted(priority_queue, key=lambda x: (x[0], x[1]))  # Sort by priority and time slot
    for i, (priority, time_slot, patient_id) in enumerate(sorted_queue, start=1):
        patients[patient_id]["queue_number"] = i

if __name__ == '__main__':
    socketio.run(app, debug=True)