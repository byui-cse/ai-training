"""
Unit tests for authentication service.
"""

import pytest
from datetime import timedelta

from app.services.auth import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)


class TestPasswordHashing:
    """Test password hashing functionality."""

    def test_password_hash_creation(self):
        """Test that password hashing works."""
        password = "testpassword123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_password_verification(self):
        """Test password verification."""
        password = "testpassword123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes."""
        hash1 = get_password_hash("password1")
        hash2 = get_password_hash("password2")

        assert hash1 != hash2


class TestJWTToken:
    """Test JWT token creation and verification."""

    def test_create_access_token(self):
        """Test access token creation."""
        subject = "123"
        token = create_access_token(subject=subject)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiry(self):
        """Test access token creation with custom expiry."""
        subject = "123"
        expires_delta = timedelta(minutes=5)
        token = create_access_token(subject=subject, expires_delta=expires_delta)

        assert isinstance(token, str)

    def test_verify_valid_token(self):
        """Test verification of valid token."""
        subject = "123"
        token = create_access_token(subject=subject)
        verified_subject = verify_token(token)

        assert verified_subject == subject

    def test_verify_invalid_token(self):
        """Test verification of invalid token."""
        invalid_token = "invalid.jwt.token"
        verified_subject = verify_token(invalid_token)

        assert verified_subject is None

    def test_create_refresh_token(self):
        """Test refresh token creation."""
        subject = "123"
        token = create_refresh_token(subject=subject)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_refresh_token(self):
        """Test refresh token verification."""
        subject = "123"
        token = create_refresh_token(subject=subject)
        verified_subject = verify_token(token)

        assert verified_subject == subject
