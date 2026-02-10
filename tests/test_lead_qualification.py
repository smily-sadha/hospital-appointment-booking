import pytest

from agent.agent import CourseLeadAgent
from agent.intent import Intent
from agent.state import LeadState
from agent.policy_engine import PolicyEngine
from agent.router import Router


@pytest.fixture
def agent():
    policy = PolicyEngine()
    router = Router()
    memory = []  # simple stub, replace later if needed
    return CourseLeadAgent(memory=memory, policy_engine=policy, router=router)


def test_exploratory_student_flow(agent):
    """
    Scenario:
    - First-year student
    - No AI experience
    - Exploring during holidays
    - Parent is decision-maker
    Expected:
    - Warm lead
    - No handoff
    - No selling
    """

    # Turn 1: student intro
    response = agent.handle_input(
        "I don't have any experience. I'm a first-year student."
    )
    assert response is not None
    assert agent.state.experience_level == "beginner"
    assert agent.state.interest_level in (None, "warm")

    # Turn 2: exploration intent
    response = agent.handle_input(
        "I'm just exploring during holidays and attending some online courses."
    )
    assert agent.state.interest_level == "warm"
    assert agent.state.qualification_complete is False
    assert agent.state.handoff_ready is False

    # Turn 3: decision authority revealed
    response = agent.handle_input(
        "I need to discuss with my parents before deciding."
    )
    assert agent.state.decision_maker == "parents"
    assert agent.state.handoff_ready is False

    # Agent must not escalate or sell
    assert "investment" not in response.lower()
    assert "price" not in response.lower()
    assert "seat" not in response.lower()


def test_price_sensitive_student(agent):
    """
    Scenario:
    - Student expresses price concern
    Expected:
    - Mark as price sensitive
    - No push
    - Continue information flow
    """

    response = agent.handle_input(
        "Spending that much doesn't feel right for me as a student."
    )

    assert agent.state.budget_sensitivity == "high"
    assert agent.state.handoff_ready is False
    assert "hold" not in response.lower()
    assert "book" not in response.lower()


def test_not_interested_exit(agent):
    """
    Scenario:
    - User is not interested
    Expected:
    - Polite exit
    - No follow-up pressure
    """

    response = agent.handle_input(
        "I'm not interested in learning AI right now."
    )

    assert agent.state.interest_level == "cold"
    assert agent.state.qualification_complete is True
    assert "thanks" in response.lower()
    assert "future" in response.lower()


def test_ready_for_counsellor_handoff(agent):
    """
    Scenario:
    - User explicitly asks to talk to admissions
    Expected:
    - Handoff allowed
    """

    # Fill minimal qualification state manually
    agent.state.course_interest = "AI"
    agent.state.experience_level = "beginner"
    agent.state.interest_level = "hot"
    agent.state.qualification_complete = True

    response = agent.handle_input(
        "I want to talk to someone from admissions for more guidance."
    )

    assert agent.state.handoff_ready is True
    assert "admissions" in response.lower()


def test_no_early_handoff(agent):
    """
    Scenario:
    - User is curious but not qualified
    Expected:
    - No handoff
    """

    response = agent.handle_input(
        "This sounds interesting, but I'm still figuring things out."
    )

    assert agent.state.interest_level == "warm"
    assert agent.state.handoff_ready is False
