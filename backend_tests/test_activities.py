"""
Tests for the activities endpoint.

Tests the GET /activities endpoint behavior, including response structure,
content, and data integrity.
"""

import pytest


class TestGetActivitiesEndpoint:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """
        Test that GET /activities returns all 9 activities.
        
        AAA Pattern:
        - Arrange: Expected activity names
        - Act: Send GET request to /activities
        - Assert: Verify all activities are in response
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Art Studio",
            "Drama Club",
            "Science Club",
            "Debate Team",
        ]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200, "Expected successful response"
        assert len(activities) == 9, "Expected exactly 9 activities"
        for activity_name in expected_activities:
            assert activity_name in activities, \
                f"Expected activity '{activity_name}' to be in response"

    def test_get_activities_response_structure(self, client):
        """
        Test that each activity has the required fields.
        
        AAA Pattern:
        - Arrange: Define required fields
        - Act: Send GET request to /activities
        - Assert: Verify response structure
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200, "Expected successful response"
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, \
                    f"Expected field '{field}' in activity '{activity_name}'"

    def test_get_activities_participants_is_list(self, client):
        """
        Test that participants field is a list of strings.
        
        AAA Pattern:
        - Arrange: No setup needed
        - Act: Send GET request to /activities
        - Assert: Verify participants is a list of strings
        """
        # Arrange
        # No specific setup needed

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200, "Expected successful response"
        for activity_name, activity_data in activities.items():
            participants = activity_data["participants"]
            assert isinstance(participants, list), \
                f"Expected 'participants' to be a list in '{activity_name}'"
            for participant in participants:
                assert isinstance(participant, str), \
                    f"Expected participant email to be string in '{activity_name}'"
                assert "@" in participant, \
                    f"Expected valid email format in '{activity_name}'"

    def test_get_activities_max_participants_is_integer(self, client):
        """
        Test that max_participants is a positive integer.
        
        AAA Pattern:
        - Arrange: No setup needed
        - Act: Send GET request to /activities
        - Assert: Verify max_participants is integer and positive
        """
        # Arrange
        # No specific setup needed

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200, "Expected successful response"
        for activity_name, activity_data in activities.items():
            max_participants = activity_data["max_participants"]
            assert isinstance(max_participants, int), \
                f"Expected 'max_participants' to be int in '{activity_name}'"
            assert max_participants > 0, \
                f"Expected positive 'max_participants' in '{activity_name}'"

    def test_get_activities_no_cache(self, client):
        """
        Test that the response includes no-store cache control header.
        
        AAA Pattern:
        - Arrange: No setup needed
        - Act: Send GET request to /activities
        - Assert: Verify Cache-Control header is set to no-store
        """
        # Arrange
        expected_cache_control = "no-store"

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200, "Expected successful response"
        cache_control = response.headers.get("cache-control")
        assert cache_control == expected_cache_control, \
            f"Expected Cache-Control: {expected_cache_control}, got {cache_control}"

    def test_get_activities_chess_club_has_initial_participants(self, client):
        """
        Test that Chess Club includes initial participants.
        
        AAA Pattern:
        - Arrange: Define expected initial participants
        - Act: Send GET request to /activities
        - Assert: Verify initial participants are present
        """
        # Arrange
        expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert response.status_code == 200, "Expected successful response"
        chess_club = activities["Chess Club"]
        for email in expected_participants:
            assert email in chess_club["participants"], \
                f"Expected {email} in Chess Club participants"


class TestActivitiesIntegration:
    """Integration tests for activities endpoint combined with signup/unregister."""

    def test_signup_modifies_activities_participants_list(self, client, sample_activity_name, sample_email):
        """
        Test that signing up for an activity adds the participant to the activities list.
        
        AAA Pattern:
        - Arrange: Get initial activities state
        - Act: Signup and then fetch activities
        - Assert: Verify participant was added
        """
        # Arrange
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[sample_activity_name]["participants"])

        # Act
        client.post(
            f"/activities/{sample_activity_name}/signup",
            params={"email": sample_email}
        )
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[sample_activity_name]["participants"]

        # Assert
        assert sample_email in updated_participants, \
            f"Expected {sample_email} to be in participants after signup"
        assert len(updated_participants) == initial_count + 1, \
            "Expected participant count to increase by 1"

    def test_unregister_modifies_activities_participants_list(self, client, sample_activity_name, existing_participant_email):
        """
        Test that unregistering removes the participant from the activities list.
        
        AAA Pattern:
        - Arrange: Get initial activities state
        - Act: Unregister and then fetch activities
        - Assert: Verify participant was removed
        """
        # Arrange
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[sample_activity_name]["participants"])
        assert existing_participant_email in initial_response.json()[sample_activity_name]["participants"]

        # Act
        client.post(
            f"/activities/{sample_activity_name}/unregister",
            params={"email": existing_participant_email}
        )
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[sample_activity_name]["participants"]

        # Assert
        assert existing_participant_email not in updated_participants, \
            f"Expected {existing_participant_email} to be removed from participants"
        assert len(updated_participants) == initial_count - 1, \
            "Expected participant count to decrease by 1"
