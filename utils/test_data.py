"""Shared test data."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    username: str
    password: str


VALID_USER = User(username="john", password="demo")
INVALID_USER = User(username="bad_user", password="bad_pass")

TRANSFER = {"from_account": "12345", "to_account": "67890", "amount": "1000"}
