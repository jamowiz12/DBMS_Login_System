"""Registration and login logic for the CLI application."""

from datetime import datetime

import bcrypt
import pyodbc

from database import get_connection


def hash_password(password):
    """Return a bcrypt hash for a plaintext password."""
    return bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt(rounds=12)
    ).decode("utf-8")


def verify_password(password, password_hash):
    """Return True when a plaintext password matches a bcrypt hash."""
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"), password_hash.encode("utf-8")
        )
    except (TypeError, ValueError):
        return False


def username_exists(username):
    """Return True when the username is already registered."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM Users WHERE Username = ?", (username,)
        )
        return cursor.fetchone()[0] > 0
    finally:
        if connection is not None:
            connection.close()


def register_user(full_name, username, password, email):
    """Validate and create a user account, returning a status and message."""
    full_name = full_name.strip()
    username = username.strip()
    email = email.strip()

    if not full_name:
        return False, "Full Name cannot be empty."
    if not username:
        return False, "Username cannot be empty."
    if len(username) < 3:
        return False, "Username must be at least 3 characters."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if not email:
        return False, "Email cannot be empty."
    if "@" not in email or "." not in email:
        return False, "Email must contain @ and ."

    try:
        if username_exists(username):
            return False, "That username is already registered."

        password_hash = hash_password(password)
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Users "
                "(FullName, Username, PasswordHash, Email, DateRegistered) "
                "VALUES (?, ?, ?, ?, ?)",
                (full_name, username, password_hash, email, datetime.now()),
            )
            connection.commit()
        finally:
            connection.close()
        return True, "Registration successful!\nYour account has been created."
    except pyodbc.IntegrityError:
        return False, "That username is already registered."
    except (FileNotFoundError, RuntimeError, ConnectionError):
        return False, "Registration could not be completed because the database is unavailable."
    except pyodbc.Error:
        return False, "Registration could not be completed because of a database error."


def login_user(username, password):
    """Return safe user information when credentials are valid, otherwise None."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT UserID, FullName, Username, PasswordHash, Email, DateRegistered "
            "FROM Users WHERE Username = ?",
            (username,),
        )
        row = cursor.fetchone()
        if row is None or not verify_password(password, row.PasswordHash):
            return None

        return {
            "user_id": row.UserID,
            "full_name": row.FullName,
            "username": row.Username,
            "email": row.Email,
            "date_registered": row.DateRegistered,
        }
    finally:
        if connection is not None:
            connection.close()