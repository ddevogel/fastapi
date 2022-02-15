import pytest
from app.config import DATABASE_URI


def test_config(monkeypatch):
    monkeypatch.setenv("DATABASE_URI", "sqlite:////code/app/database/chinook.db")
    assert DATABASE_URI == "sqlite:////code/app/database/chinook.db"
