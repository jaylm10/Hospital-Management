# Hospital Management System

This project is a **Hospital Management System** built using **Flask** (Python) and **Socket.IO** for real-time updates. It allows patients to register, describe their symptoms, and get a queue number. Doctors can view the patient queue in real-time and manage appointments efficiently.

---

## Features

### **Patient Features**
- **Registration**: Patients can register by providing their details (name, age, contact, address, and preferred time slot).
- **Symptoms Submission**: Patients can describe their symptoms and select an urgency level (high, medium, low).
- **Queue Number**: Patients receive a queue number and can see how many patients are ahead of them.
- **Real-Time Updates**: Queue numbers are updated in real-time if a higher-priority patient arrives.

### **Doctor Features**
- **Real-Time Dashboard**: Doctors can view the list of patients sorted by priority and time slot.
- **Close Patient**: Doctors can mark a patient as "treated," which removes them from the queue and updates the queue numbers for the remaining patients.

---

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Real-Time Communication**: Socket.IO
- **Data Structures**: Priority Queue (Min-Heap) for managing patient appointments
- **Database**: In-memory Python dictionaries (for simplicity; can be replaced with a database like SQLite or MySQL)

---

## How It Works

1. **Patient Registration**:
   - Patients fill out a registration form with their details and preferred time slot.
   - They are assigned a unique `patient_id`.

2. **Symptoms Submission**:
   - Patients describe their symptoms and select an urgency level.
   - The system assigns a queue number based on the urgency level and time slot.

3. **Doctor Dashboard**:
   - Doctors can view the list of patients sorted by priority and time slot.
   - They can close a patient, which removes them from the queue and updates the queue numbers for the remaining patients.

4. **Real-Time Updates**:
   - The system uses **Socket.IO** to push updates to the frontend whenever the queue changes.

