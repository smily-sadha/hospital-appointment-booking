import re
from datetime import datetime, timedelta


# --------------------------------------------------
# BASIC INTENTS
# --------------------------------------------------

def is_booking(text: str) -> bool:
    return any(
        k in text for k in
        ["book", "appointment", "consult", "visit doctor"]
    )


def is_reschedule(text: str) -> bool:
    return any(
        k in text for k in
        ["reschedule", "change appointment", "postpone"]
    )


def is_cancel(text: str) -> bool:
    return any(
        k in text for k in
        ["cancel", "cancel appointment", "drop appointment"]
    )


def is_yes(text: str) -> bool:
    return any(
        k in text for k in
        ["yes", "yeah", "yep", "correct", "right", "okay", "ok"]
    )


def is_no(text: str) -> bool:
    return any(
        k in text for k in
        ["no", "not", "wrong", "incorrect"]
    )


# --------------------------------------------------
# ENTITY EXTRACTION
# --------------------------------------------------

def extract_department(text: str):
    departments = [
        "cardiology",
        "orthopedics",
        "neurology",
        "dermatology",
        "ent",
        "general medicine",
        "pediatrics",
        "gynecology",
    ]

    for dept in departments:
        if dept in text:
            return dept.title()

    return None


def extract_doctor_name(text: str, doctors: list):
    """
    Robust doctor name extraction for voice input.
    Handles:
    - "Yes doctor kumar"
    - "Doctor Kumar"
    - "Dr Kumar"
    - "Kumar"
    """

    clean = text.lower()

    # remove filler words
    for junk in ["yes", "doctor", "dr", ".", ","]:
        clean = clean.replace(junk, " ")

    clean = re.sub(r"\s+", " ", clean).strip()

    for d in doctors:
        # normalize stored doctor name
        name_tokens = (
            d["name"]
            .lower()
            .replace("dr", "")
            .replace(".", "")
            .split()
        )

        # match if all tokens appear anywhere
        if all(token in clean for token in name_tokens):
            return d["name"]

    return None


def extract_patient_name(text: str):
    patterns = [
        r"name is ([a-zA-Z ]+)",
        r"patient name is ([a-zA-Z ]+)",
        r"this is ([a-zA-Z ]+)",
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(1).strip().title()

    words = text.split()
    if 1 <= len(words) <= 3:
        return " ".join(words).title()

    return None


def extract_date(text: str):
    text = text.lower()

    if "today" in text:
        return datetime.now().strftime("%Y-%m-%d")

    if "tomorrow" in text:
        return (
            datetime.now().replace(hour=0)
            + timedelta(days=1)
        ).strftime("%Y-%m-%d")

    match = re.search(
        r"(\d{1,2})\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)",
        text
    )
    if match:
        day = int(match.group(1))
        month = match.group(2)
        year = datetime.now().year
        try:
            date = datetime.strptime(
                f"{day} {month} {year}", "%d %b %Y"
            )
            return date.strftime("%Y-%m-%d")
        except:
            return None

    return None


def extract_slot(text: str, slots: list):
    """
    Voice-safe slot matching.
    Matches: '9AM', '9 AM', '9', '9am is fine'
    """
    clean = text.lower().replace(" ", "")

    for slot in slots:
        # "9:00 AM" -> hour = "9"
        hour = slot.split(":")[0].lower()

        if hour in clean:
            return slot

    return None
