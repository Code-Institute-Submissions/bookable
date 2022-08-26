"""Tests Fixtures"""
import pytest


@pytest.fixture
def user_client(django_user_model):
    """User Fixture"""
    username = "user1"
    password = "testpass123"

    user = django_user_model.objects.create_user(username=username, password=password)

    return user
