"""
Intent & entity extraction for Hospital Appointment Agent
Voice-safe, tolerant parsing
"""

import re


# ---------------------------
# BASIC YES / NO
# ---------------------------

def is_yes(text: str) -> bool:
    return any(k in text for k in [
        "yes", "yeah", "yep", "sure", "ok", "okay"
    ])


def is_no(text: str) -> bool:
    return any(k in text for k in [
        "no", "not interested", "cancel", "don't"
    ])


# ---------------------------
# HIGH-LEVEL INTENT
# ---------------------------

def is_booking(text: str) -> bool:
    return any(k in text for k in [
        "book", "appointment", "consult"
    ])


def is_reschedule(text: str) -> bool:
    return any(k in text for k in [
        "reschedule", "change"
    ])


def is_cancel(text: str) -> bool:
    return any(k in text for k in [
        "cancel", "delete"
    ])


# ---------------------------
# ENTITY EXTRACTION
# ---------------------------

def extract_department(text: str):
    departments = ["cardiology", "orthopedics", "dermatology", "neurology"]
    for dept in departments:
        if dept in text:
            return dept.capitalize()
    return None


def extract_doctor(text: str, doctors: list):
    for doc in doctors:
        if doc.lower() in text:
            return doc
    return None


def extract_date(text: str):
    # Simple placeholder — you can improve later
    return text if text else None


# ---------------------------
# ✅ FIXED SLOT EXTRACTION
# ---------------------------

def extract_slot(user_text: str, available_slots: list):
    """
    Match spoken time like:
    - '11AM'
    - '11 am'
    - '11'
    - '11:30'
    against slots like:
    - '11:00 AM'
    - '11:30 AM'
    """

    user_text = user_text.lower().replace(" ", "")

    # Extract hour and optional minutes
    match = re.search(r"(\d{1,2})(?::(\d{2}))?(am|pm)?", user_text)
    if not match:
        return None

    hour = int(match.group(1))
    minutes = match.group(2) or "00"
    period = match.group(3) or ""

    # Normalize user slot to canonical form
    user_key = f"{hour}:{minutes}{period}"

    for slot in available_slots:
        # Normalize slot label
        slot_norm = slot.lower().replace(" ", "")
        slot_match = re.search(r"(\d{1,2}):(\d{2})(am|pm)", slot_norm)

        if not slot_match:
            continue

        slot_hour = int(slot_match.group(1))
        slot_min = slot_match.group(2)
        slot_period = slot_match.group(3)

        slot_key = f"{slot_hour}:{slot_min}{slot_period}"

        # Match hour + period (ignore minutes if user didn’t say them)
        if period:
            if slot_key.startswith(f"{hour}:") and slot_period == period:
                return slot
        else:
            if slot_hour == hour:
                return slot

    return None
