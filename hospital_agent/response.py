"""
Response templates for Hospital Appointment Agent
Polite, neutral, healthcare-appropriate
"""


def opening():
    return (
        "Hello, this is the appointment desk calling from the hospital. "
        "Are you calling to book a doctor appointment?"
    )


def confirm_purpose_retry():
    return "Just to confirm, are you looking to book a hospital appointment?"


def ask_department():
    return (
        "Alright. Which department or doctor would you like to book an appointment with?"
    )


def ask_date(department: str):
    return (
        f"Got it. When would you like to schedule the appointment for the {department} department?"
    )


def ask_time():
    return (
        "Thank you. Do you have a preferred time for the appointment? "
        "For example, morning or afternoon."
    )


def confirm_details(department: str, date: str, time: str):
    return (
        f"Just to confirm, you would like to book an appointment with the "
        f"{department} department on {date} at {time}. Is that correct?"
    )


def booking_success():
    return (
        "Your appointment has been noted. "
        "Our team will confirm the booking shortly. "
        "Thank you for choosing our hospital. Take care."
    )


def close():
    return "Thank you. Have a good day."
