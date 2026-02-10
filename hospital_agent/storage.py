"""
Simple file-based appointment storage
"""

import json
import os
from datetime import datetime

DATA_FILE = "appointments.json"


def _load_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def generate_appointment_id():
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"APT-{ts}"


def save_appointment(appointment: dict):
    data = _load_data()
    data.append(appointment)
    _save_data(data)


def find_appointment_by_name(name: str):
    data = _load_data()
    for appt in data:
        if appt["patient_name"].lower() == name.lower() and appt["status"] == "CONFIRMED":
            return appt
    return None


def update_appointment(appointment_id: str, updates: dict):
    data = _load_data()
    for appt in data:
        if appt["appointment_id"] == appointment_id:
            appt.update(updates)
            break
    _save_data(data)
