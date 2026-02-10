from enum import Enum


class ConversationState(Enum):
    OPENING = "opening"
    INTENT_SELECTION = "intent_selection"

    COLLECT_PATIENT_NAME = "collect_patient_name"   # NEW

    COLLECT_DEPARTMENT = "collect_department"
    SELECT_DOCTOR_PREFERENCE = "select_doctor_preference"
    COLLECT_DATE = "collect_date"
    OFFER_SLOTS = "offer_slots"
    CONFIRM_DETAILS = "confirm_details"

    RESCHEDULE_CONFIRM = "reschedule_confirm"
    CANCEL_CONFIRM = "cancel_confirm"

    CLOSE = "close"
