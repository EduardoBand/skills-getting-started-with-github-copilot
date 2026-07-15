"""
Tests for the signup and unregister endpoints.

Tests for POST /activities/{activity_name}/signup and 
POST /activities/{activity_name}/unregister endpoints.
"""

import pytest


class TestSignupEndpoint:
    """Test suite for the signup endpoint (POST /activities/{activity_name}/signup)."""

    def test_signup_with_valid_email_adds_participant(self, client, sample_activity_name, sample_email):
        """
        Test that signing up with valid email successfully adds participant.
        
        AAA Pattern:
        - Arrange: Prepare test data
        - Act: Send POST request to signup endpoint
        - Assert: Verify success response and email is added
        """
        # Arrange
        activity_name = sample_activity_name
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200, "Expected successful signup"
        assert "message" in response.json(), "Expected message in response"
        assert email in response.json()["message"], \
            "Expected email to be mentioned in success message"
        assert activity_name in response.json()["message"], \
            "Expected activity name in success message"

    def test_signup_nonexistent_activity_returns_404(self, client, sample_email):
        """
        Test that signing up for a nonexistent activity returns 404.
        
        AAA Pattern:
        - Arrange: Use a fake activity name
        - Act: Send POST request to signup with nonexistent activity
        - Assert: Verify 404 error
        """
        # Arrange
        fake_activity = "Nonexistent Activity"
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{fake_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404, "Expected 404 for nonexistent activity"
        assert "Activity not found" in response.json()["detail"], \
            "Expected 'Activity not found' in error message"

    def test_signup_duplicate_email_returns_400(self, client, sample_activity_name, existing_participant_email):
        """
        Test that signing up with an email already registered returns 400.
        
        AAA Pattern:
        - Arrange: Use email already in activity
        - Act: Try to signup with duplicate email
        - Assert: Verify 400 error
        """
        # Arrange
        activity_name = sample_activity_name
        email = existing_participant_email  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400, "Expected 400 for duplicate signup"
        assert "already signed up" in response.json()["detail"], \
            "Expected 'already signed up' in error message"

    def test_signup_multiple_activities_same_email(self, client, sample_email):
        """
        Test that same email can signup for multiple different activities.
        
        AAA Pattern:
        - Arrange: Test data for two activities
        - Act: Signup for two different activities with same email
        - Assert: Verify both signups succeed
        """
        # Arrange
        email = sample_email
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )

        # Assert
        assert response1.status_code == 200, f"Expected successful signup for {activity1}"
        assert response2.status_code == 200, f"Expected successful signup for {activity2}"

        # Verify both signups are recorded
        activities = client.get("/activities").json()
        assert email in activities[activity1]["participants"], \
            f"Expected {email} in {activity1} participants"
        assert email in activities[activity2]["participants"], \
            f"Expected {email} in {activity2} participants"

    def test_signup_response_format(self, client, sample_activity_name, sample_email):
        """
        Test that signup response has correct JSON format.
        
        AAA Pattern:
        - Arrange: Test data
        - Act: Send signup request
        - Assert: Verify response JSON structure
        """
        # Arrange
        activity_name = sample_activity_name
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert isinstance(data, dict), "Expected response to be a dictionary"
        assert "message" in data, "Expected 'message' key in response"
        assert isinstance(data["message"], str), "Expected message to be a string"


class TestUnregisterEndpoint:
    """Test suite for the unregister endpoint (POST /activities/{activity_name}/unregister)."""

    def test_unregister_removes_participant(self, client, sample_activity_name, existing_participant_email):
        """
        Test that unregistering successfully removes participant from activity.
        
        This is the consolidation of the existing test:
        test_unregister_participant_removes_email_from_activity
        
        AAA Pattern:
        - Arrange: Prepare test data with existing participant
        - Act: Send POST request to unregister endpoint
        - Assert: Verify success response and email is removed
        """
        # Arrange
        activity_name = sample_activity_name
        email = existing_participant_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200, "Expected successful unregister"
        assert "Unregistered" in response.json()["message"], \
            "Expected 'Unregistered' in response message"
        assert email in response.json()["message"], \
            "Expected email in success message"

        # Verify removal from activities list
        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"], \
            f"Expected {email} to be removed from {activity_name} participants"

    def test_unregister_nonexistent_activity_returns_404(self, client, sample_email):
        """
        Test that unregistering from nonexistent activity returns 404.
        
        AAA Pattern:
        - Arrange: Use fake activity name
        - Act: Send POST request to unregister with nonexistent activity
        - Assert: Verify 404 error
        """
        # Arrange
        fake_activity = "Nonexistent Activity"
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{fake_activity}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404, "Expected 404 for nonexistent activity"
        assert "Activity not found" in response.json()["detail"], \
            "Expected 'Activity not found' in error message"

    def test_unregister_nonparticipant_returns_404(self, client, sample_activity_name, sample_email):
        """
        Test that unregistering non-participating email returns 404.
        
        AAA Pattern:
        - Arrange: Use email not in activity
        - Act: Try to unregister non-participant
        - Assert: Verify 404 error
        """
        # Arrange
        activity_name = sample_activity_name
        email = sample_email  # Not registered yet

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404, "Expected 404 for non-participant"
        assert "not signed up" in response.json()["detail"], \
            "Expected 'not signed up' in error message"

    def test_unregister_response_format(self, client, sample_activity_name, existing_participant_email):
        """
        Test that unregister response has correct JSON format.
        
        AAA Pattern:
        - Arrange: Test data
        - Act: Send unregister request
        - Assert: Verify response JSON structure
        """
        # Arrange
        activity_name = sample_activity_name
        email = existing_participant_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert isinstance(data, dict), "Expected response to be a dictionary"
        assert "message" in data, "Expected 'message' key in response"
        assert isinstance(data["message"], str), "Expected message to be a string"


class TestSignupUnregisterIntegration:
    """Integration tests combining signup and unregister operations."""

    def test_signup_then_unregister_workflow(self, client, sample_activity_name, sample_email):
        """
        Test complete signup and unregister workflow.
        
        AAA Pattern:
        - Arrange: Prepare test data
        - Act: Signup, verify in list, then unregister
        - Assert: Verify state at each step
        """
        # Arrange
        activity_name = sample_activity_name
        email = sample_email

        # Act & Assert - Signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200, "Expected successful signup"

        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"], \
            "Expected email in participants after signup"

        # Act & Assert - Unregister
        unregister_response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200, "Expected successful unregister"

        activities = client.get("/activities").json()
        assert email not in activities[activity_name]["participants"], \
            "Expected email removed from participants after unregister"

    def test_signup_duplicate_after_unregister_allowed(self, client, sample_activity_name, existing_participant_email):
        """
        Test that after unregistering, can signup again with same email.
        
        AAA Pattern:
        - Arrange: Prepare participant who will unregister
        - Act: Unregister, then signup again
        - Assert: Verify second signup succeeds
        """
        # Arrange
        activity_name = sample_activity_name
        email = existing_participant_email

        # Act & Assert - Unregister first
        unregister_response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == 200, "Expected successful unregister"

        # Act & Assert - Signup again with same email
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200, "Expected successful re-signup after unregister"

        # Verify in participants list
        activities = client.get("/activities").json()
        assert email in activities[activity_name]["participants"], \
            "Expected email in participants after re-signup"
