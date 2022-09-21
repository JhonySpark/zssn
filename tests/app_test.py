from app import app
import pytest

def test_main():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert response.data == b"Welcome to the ZSSN Survivors API!"