"""Microsoft Access database connection helpers."""

from pathlib import Path

import pyodbc


DATABASE_FILENAME = "UserSystem.accdb"
ACCESS_DRIVER = "Microsoft Access Driver (*.mdb, *.accdb)"
DATABASE_PATH = Path(__file__).resolve().parent / DATABASE_FILENAME


def driver_is_available():
    """Return True when the required Microsoft Access ODBC driver is installed."""
    return ACCESS_DRIVER in pyodbc.drivers()


def get_connection():
    """Open and return a connection to the project Access database."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Database file not found: {DATABASE_PATH}. "
            "Create UserSystem.accdb in the project folder using Microsoft Access."
        )

    if not driver_is_available():
        raise RuntimeError(
            "Microsoft Access Driver (*.mdb, *.accdb) is not installed. "
            "Install the Microsoft Access Database Engine and make sure Python "
            "and the driver use matching 32-bit or 64-bit architecture."
        )

    connection_string = f"DRIVER={{{ACCESS_DRIVER}}};DBQ={DATABASE_PATH};"

    try:
        return pyodbc.connect(connection_string)
    except pyodbc.Error as error:
        raise ConnectionError(
            "Could not connect to UserSystem.accdb. Check the database file, "
            "table structure, and Access driver installation."
        ) from error


def test_connection():
    """Test the database and print the number of registered users."""
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users")
        total_users = cursor.fetchone()[0]
        print("Database connected successfully!")
        print(f"Total users in database: {total_users}")
        return True
    except (FileNotFoundError, RuntimeError, ConnectionError) as error:
        print(f"Database connection failed: {error}")
        return False
    except pyodbc.Error as error:
        print("Database connection failed while reading the Users table.")
        print(f"Developer details: {error}")
        return False
    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    test_connection()