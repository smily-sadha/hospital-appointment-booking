"""
Hospital Appointment Booking Agent
Final wording fix: availability stated before asking date
"""

from hospital_agent.state import ConversationState
from hospital_agent.intent import (
    is_booking,
    is_yes,
    extract_department,
    extract_doctor_name,
    extract_date,
    extract_slot,
    extract_patient_name,
)
from hospital_agent.availability import get_doctors, get_available_slots
from hospital_agent.storage import save_appointment, generate_appointment_id


class HospitalAppointmentAgent:
    def __init__(self, memory):
        self.memory = memory
        self.state = ConversationState.INTENT_SELECTION
        self.context = {}

    # ==================================================
    # ENTRY
    # ==================================================

    def handle_input(self, user_text: str) -> str:
        text = user_text.lower().strip()
        self.memory.add_message("user", user_text)
        if "fee" in text or "fees" in text or "consultation" in text:
                doctor = self._resolve_doctor(text)
                if doctor:
                    return f"The consultation fee for {doctor['name']} is {doctor['fee']} rupees."
                return "I couldn't find that doctor in our records."

        if self.state == ConversationState.INTENT_SELECTION:
            return self._intent_selection(text)

        if self.state == ConversationState.COLLECT_DEPARTMENT:
            return self._collect_department(text)

        if self.state == ConversationState.SELECT_DOCTOR:
            return self._select_doctor(text)

        if self.state == ConversationState.CONFIRM_APPOINTMENT:
            return self._confirm_after_experience(text)

        if self.state == ConversationState.COLLECT_DATE:
            return self._collect_date(text)

        if self.state == ConversationState.OFFER_SLOTS:
            return self._offer_slots(text)

        if self.state == ConversationState.COLLECT_PATIENT_NAME:
            return self._collect_patient_name(text)

        return self._close()

    # ==================================================
    # INTENT
    # ==================================================

    def _intent_selection(self, text):
        if is_booking(text):
            dept = extract_department(text)
            if dept:
                self.context["department"] = dept
                return self._department_availability()

            self.state = ConversationState.COLLECT_DEPARTMENT
            return "Which department would you like to consult?"

        return "How may I help you with your appointment today?"

    # ==================================================
    # DEPARTMENT
    # ==================================================

    def _collect_department(self, text):
        dept = extract_department(text)
        if not dept:
            return "Please tell me the department name."

        self.context["department"] = dept
        return self._department_availability()

    def _department_availability(self):
        doctors = get_doctors(self.context["department"])
        self.context["doctors"] = doctors
        self.state = ConversationState.SELECT_DOCTOR

        names = ", ".join(d["name"] for d in doctors)
        return (
            "let me look the Available doctors in this department are "
            f"{names}. "
            "Do you have a preferred doctor?"
        )

    # ==================================================
    # DOCTOR
    # ==================================================

    def _select_doctor(self, text):
        doctors = self.context["doctors"]

        # Explicit doctor
        name = extract_doctor_name(text, doctors)
        if name:
            doctor = next(d for d in doctors if d["name"] == name)
            self.context["doctor"] = doctor
            self.state = ConversationState.COLLECT_DATE

            return (
                f"{doctor['name']} is available. "
                "Do you have a specific date you would like to visit?"
            )

        # Senior doctor
        if any(k in text for k in ["senior", "experienced", "most experienced", "best"]):
            doctor = max(doctors, key=lambda d: d["experience"])
            self.context["doctor"] = doctor
            self.state = ConversationState.CONFIRM_APPOINTMENT

            return (
                f"{doctor['name']} has {doctor['experience']} years of experience "
                "and is the most experienced doctor in this department. "
                f"Would you like to book an appointment with {doctor['name']}?"
            )

        return "Please tell me the doctor’s name."

    # ==================================================
    # CONFIRM
    # ==================================================

    def _confirm_after_experience(self, text):
        if is_yes(text):
            self.state = ConversationState.COLLECT_DATE
            d = self.context["doctor"]
            return (
                f"{d['name']} is available. "
                "Do you have a specific date you would like to visit?"
            )

        self.state = ConversationState.SELECT_DOCTOR
        return "Alright. Would you like to choose another doctor?"

    # ==================================================
    # DATE
    # ==================================================

    def _collect_date(self, text):
        date = extract_date(text)
        if not date:
            return "Please tell me the exact date you would like to visit."

        self.context["date"] = date
        slots = get_available_slots(self.context["doctor"])
        self.context["slots"] = slots
        self.state = ConversationState.OFFER_SLOTS

        return f"Available slots on {date} are {', '.join(slots)}. Which one works?"

    # ==================================================
    # SLOT
    # ==================================================

    def _offer_slots(self, text):
        slot = extract_slot(text, self.context["slots"])
        if not slot:
            return "Please select one of the available time slots."

        self.context["time"] = slot
        self.state = ConversationState.COLLECT_PATIENT_NAME
        return "May I have the patient’s full name to confirm the booking?"

    # ==================================================
    # PATIENT
    # ==================================================

    def _collect_patient_name(self, text):
        name = extract_patient_name(text)
        if not name:
            return "Please repeat the patient’s full name."

        appt_id = generate_appointment_id()
        save_appointment({
            "appointment_id": appt_id,
            "patient_name": name,
            "doctor": self.context["doctor"]["name"],
            "department": self.context["department"],
            "date": self.context["date"],
            "time": self.context["time"],
            "status": "CONFIRMED",
        })

        return (
            f"Your appointment is confirmed. "
            f"Your appointment ID is {appt_id}. "
            "We look forward to seeing you."
        )

    def _close(self):
        return "Thank you for calling CityCare Hospital. Have a pleasant day."
