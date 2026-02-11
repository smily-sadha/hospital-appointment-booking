from enum import Enum


class ConversationState(Enum):
    OPENING = "opening"

    INTENT_SELECTION = "intent_selection"

    COLLECT_DEPARTMENT = "collect_department"
    SELECT_DOCTOR = "select_doctor"

    COLLECT_DATE = "collect_date"
    OFFER_SLOTS = "offer_slots"

    CONFIRM_APPOINTMENT = "confirm_appointment"
    COLLECT_PATIENT_NAME = "collect_patient_name"

    RESCHEDULE_FLOW = "reschedule_flow"
    CANCEL_FLOW = "cancel_flow"

    CLOSE = "close"
