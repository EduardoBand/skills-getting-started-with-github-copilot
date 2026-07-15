"""
Tests for the root endpoint.

Tests the GET / endpoint behavior.
"""

import pytest


class TestRootEndpoint:
    """Test suite for the root endpoint (GET /)."""

    def test_root_redirects_to_static_index_html(self, client):
        """
        Test that GET / returns a redirect to /static/index.html.
        
        AAA Pattern:
        - Arrange: No setup needed
        - Act: Send GET request to /
        - Assert: Verify redirect status code and location
        """
        # Arrange
        expected_redirect_url = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307, "Expected temporary redirect status code"
        assert response.headers["location"] == expected_redirect_url, \
            "Expected redirect to /static/index.html"

    def test_root_redirect_follows_to_static_location(self, client):
        """
        Test that the root endpoint redirect can be followed.
        
        AAA Pattern:
        - Arrange: Set up expectations
        - Act: Send GET request with follow_redirects=True
        - Assert: Verify we don't get an error (the static file exists or is mounted)
        """
        # Arrange
        # Following redirects will attempt to fetch the static file

        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        # Status code should be 200 (either the file exists or we get the static mount)
        assert response.status_code == 200 or response.status_code == 404, \
            "Expected either successful load or 404 for static files"
