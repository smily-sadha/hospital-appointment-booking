"""
Hospital Appointment Booking Agent
Name-only patient identification
"""

from hospital_agent.state import ConversationState
from hospital_agent.intent import (
    is_yes,
    is_no,
    is_booking,
    is_reschedule,
    is_cancel,
    extract_patient_name,
    extract_department,
    extract_date,
    extract_slot,
)
from hospital_agent.availability import get_doctors, get_available_slots
from hospital_agent.storage import (
    save_appointment,
    find_appointment_by_name,
    update_appointment,
    generate_appointment_id,
)



class HospitalAppointmentAgent:
    def __init__(self, memory):
        self.memory = memory
        self.state = ConversationState.OPENING
        self.context = {}

    # --------------------------------------------------

    def handle_input(self, user_text: str) -> str:
        text = user_text.lower().strip()
        self.memory.add_message("user", user_text)

        if self.state == ConversationState.OPENING:
            response = self._opening()

        elif self.state == ConversationState.INTENT_SELECTION:
            response = self._intent_selection(text)

        elif self.state == ConversationState.COLLECT_PATIENT_NAME:
            response = self._collect_patient_name(text)

        elif self.state == ConversationState.COLLECT_DEPARTMENT:
            response = self._collect_department(text)

        elif self.state == ConversationState.SELECT_DOCTOR_PREFERENCE:
            response = self._select_doctor_preference(text)

        elif self.state == ConversationState.COLLECT_DATE:
            response = self._collect_date(text)

        elif self.state == ConversationState.OFFER_SLOTS:
            response = self._offer_slots(text)

        elif self.state == ConversationState.CONFIRM_DETAILS:
            response = self._confirm_booking(text)

        elif self.state == ConversationState.RESCHEDULE_CONFIRM:
            response = self._reschedule_confirm(text)

        elif self.state == ConversationState.CANCEL_CONFIRM:
            response = self._cancel_confirm(text)

        else:
            response = self._close()

        self.memory.add_message("agent", response)
        return response

    # --------------------------------------------------

    def _opening(self):
        self.state = ConversationState.INTENT_SELECTION
        return (
            "Hello, this is the hospital appointment desk. "
            "Would you like to book, reschedule, or cancel an appointment?"
        )

    def _intent_selection(self, text):
        if is_booking(text) or is_reschedule(text) or is_cancel(text):
            self.context["intent"] = text
            self.state = ConversationState.COLLECT_PATIENT_NAME
            return "Sure. May I have the patient name, please?"

        return "Please tell me if you want to book, reschedule, or cancel an appointment."

    # ---------------- NAME ----------------

    def _collect_patient_name(self, text):
        name = extract_patient_name(text)
        if not name:
            return "Sorry, I didn’t catch the name. Could you please repeat it?"

        self.context["patient_name"] = name

        if is_reschedule(self.context["intent"]):
            self.state = ConversationState.RESCHEDULE_CONFIRM
            return f"Thanks {name}. Would you like to reschedule the appointment?"

        if is_cancel(self.context["intent"]):
            self.state = ConversationState.CANCEL_CONFIRM
            return f"Thanks {name}. Would you like to cancel the appointment?"

        self.state = ConversationState.COLLECT_DEPARTMENT
        return f"Thanks {name}. Which department would you like to consult?"

    # ---------------- BOOKING FLOW ----------------

    def _collect_department(self, text):
        dept = extract_department(text)
        if not dept:
            return "Please tell me the department."

        self.context["department"] = dept
        self.context["doctors"] = get_doctors(dept)
        self.state = ConversationState.SELECT_DOCTOR_PREFERENCE

        return (
            "Do you have a preference for a senior doctor, "
            "a lower consultation fee, or a specific doctor?"
        )

    def _select_doctor_preference(self, text):
        doctors = self.context["doctors"]

        for d in doctors:
            if d["name"].lower().replace(".", "") in text.replace(".", ""):
                self.context["doctor"] = d
                self.state = ConversationState.COLLECT_DATE
                return f"When would you like to visit {d['name']}?"

        selected = max(doctors, key=lambda d: d["experience"])
        self.context["doctor"] = selected
        self.state = ConversationState.COLLECT_DATE
        return (
            f"I recommend {selected['name']}. "
            f"When would you like to visit?"
        )

    def _collect_date(self, text):
        date = extract_date(text)
        if not date:
            return "Please tell me the appointment date."

        self.context["date"] = date
        slots = get_available_slots(self.context["doctor"])

        if not slots:
            self.state = ConversationState.SELECT_DOCTOR_PREFERENCE
            return (
                f"{self.context['doctor']['name']} is not available that day. "
                "Would you like to choose another doctor?"
            )

        self.context["slots"] = slots
        self.state = ConversationState.OFFER_SLOTS
        return f"Available slots on {date} are {', '.join(slots)}. Which one works?"

    def _offer_slots(self, text):
        slot = extract_slot(text, self.context["slots"])
        if not slot:
            return "Please select one of the available time slots."

        self.context["time"] = slot
        self.state = ConversationState.CONFIRM_DETAILS
        return self._summary()

    def _confirm_booking(self, text):
        if is_yes(text):
            appointment = {
                "appointment_id": generate_appointment_id(),
                "patient_name": self.context["patient_name"],
                "department": self.context["department"],
                "doctor": self.context["doctor"]["name"],
                "date": self.context["date"],
                "time": self.context["time"],
                "status": "CONFIRMED",
            }

            save_appointment(appointment)

            self.state = ConversationState.CLOSE
            return (
                f"Thank you {self.context['patient_name']}. "
                "Your appointment has been successfully booked. "
                "We look forward to seeing you."
            )

        if is_no(text):
            self.state = ConversationState.COLLECT_DATE
            return "Alright, let’s choose a different date."

        return "Please confirm if the appointment details are correct."


    # ---------------- RESCHEDULE ----------------

    def _reschedule_confirm(self, text):
        if is_yes(text):
            appt = find_appointment_by_name(self.context["patient_name"])

            if not appt:
                self.state = ConversationState.CLOSE
                return (
                    "I couldn’t find an existing appointment under your name. "
                    "Please contact the hospital desk directly."
                )

            self.context["existing_appointment"] = appt
            self.state = ConversationState.COLLECT_DEPARTMENT
            return "Sure. Let’s reschedule. Which department is the appointment with?"

        self.state = ConversationState.CLOSE
        return "No problem. Let us know if you need help later."


    # ---------------- CANCEL ----------------

    def _cancel_confirm(self, text):
        if is_yes(text):
            appt = find_appointment_by_name(self.context["patient_name"])

            if not appt:
                self.state = ConversationState.CLOSE
                return (
                    "I couldn’t find an appointment under your name. "
                    "Please contact the hospital desk for assistance."
                )

            update_appointment(
                appt["appointment_id"],
                {"status": "CANCELLED"}
            )

            self.state = ConversationState.CLOSE
            return f"Your appointment has been cancelled, {self.context['patient_name']}."

        self.state = ConversationState.CLOSE
        return "Alright. Your appointment remains unchanged."


    # --------------------------------------------------

    def _summary(self):
        return (
            f"To confirm, {self.context['patient_name']}, your appointment with "
            f"{self.context['doctor']['name']} from {self.context['department']} "
            f"is scheduled on {self.context['date']} at {self.context['time']}. "
            "Is that correct?"
        )

    def _close(self):
        return "Thank you for calling. Have a good day."
