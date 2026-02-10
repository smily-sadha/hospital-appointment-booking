"""
Doctor-wise Availability with Experience and Fees
"""

AVAILABILITY = {
    "Cardiology": [
        {
            "name": "Dr. Kumar",
            "experience": 15,
            "fee": 800,
            "slots": {
                "morning": ["9:00 AM", "10:30 AM"],
                "afternoon": ["2:00 PM"]
            }
        },
        {
            "name": "Dr. Mehta",
            "experience": 8,
            "fee": 600,
            "slots": {
                "morning": ["11:00 AM"],
                "afternoon": ["3:30 PM"]
            }
        },
        {
            "name": "Dr. Shah",
            "experience": 4,
            "fee": 400,
            "slots": {
                "afternoon": ["4:30 PM"]
            }
        }
    ],
    "General": [
        {
            "name": "Dr. Sharma",
            "experience": 12,
            "fee": 500,
            "slots": {
                "morning": ["9:00 AM", "11:00 AM"],
                "afternoon": ["2:00 PM"]
            }
        },
        {
            "name": "Dr. Verma",
            "experience": 6,
            "fee": 350,
            "slots": {
                "afternoon": ["5:00 PM"]
            }
        }
    ]
}


def get_doctors(department: str) -> list[dict]:
    return AVAILABILITY.get(department, [])


def get_available_slots(doctor: dict) -> list[str]:
    slots = []
    for times in doctor["slots"].values():
        slots.extend(times)
    return slots
