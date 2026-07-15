"""
Pytest configuration and shared fixtures for backend tests.

Provides fixtures for API testing including TestClient and test data setup.
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


# Sample test email addresses
TEST_EMAILS = {
    "student_1": "student1@mergington.edu",
    "student_2": "student2@mergington.edu",
    "student_3": "student3@mergington.edu",
    "new_student": "newstudent@mergington.edu",
}

# Store the original activities state to reset between tests
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """
    Fixture providing a TestClient instance for the FastAPI app.
    
    This fixture is function-scoped, meaning a fresh client is created
    for each test function.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Fixture that resets the activities database to its original state
    before each test. This ensures test isolation and prevents state
    pollution between tests.
    
    This fixture is automatically used (autouse=True) for all tests.
    """
    # Reset to original state before each test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    yield
    # Optional: reset after test as well for cleanliness
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def sample_activity_name():
    """Fixture providing a valid activity name for testing."""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Fixture providing a new student email for testing."""
    return TEST_EMAILS["new_student"]


@pytest.fixture
def existing_participant_email():
    """Fixture providing an email that's already registered in Chess Club."""
    return "michael@mergington.edu"
