"""Command-line controller for the user authentication system."""

import getpass

from auth import login_user, register_user


def print_heading(title):
    """Print a consistent section heading."""
    print("\n" + "=" * 40)
    print(title.center(40))
    print("=" * 40)


def registration_screen():
    """Collect registration details and display the result."""
    print_heading("REGISTER NEW ACCOUNT")
    full_name = input("Full Name: ").strip()
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")
    email = input("Email: ").strip()

    if password != confirm_password:
        print("Registration failed: Passwords do not match.")
        return

    success, message = register_user(full_name, username, password, email)
    print(message)


def profile_screen(user):
    """Display non-sensitive information for the logged-in user."""
    print_heading("MY PROFILE")
    print(f"User ID: {user['user_id']}")
    print(f"Full Name: {user['full_name']}")
    print(f"Username: {user['username']}")
    print(f"Email: {user['email']}")
    print(f"Date Registered: {user['date_registered']}")
    print("=" * 40)


def dashboard(user):
    """Show the dashboard until the user logs out."""
    while True:
        print_heading("DASHBOARD")
        print(f"Welcome, {user['full_name']}!")
        print("\n1. View Profile")
        print("2. Logout")
        choice = input("Select an option: ").strip()

        if choice == "1":
            profile_screen(user)
        elif choice == "2":
            print("Logged out successfully.")
            return
        else:
            print("Invalid option. Please choose 1 or 2.")


def login_screen():
    """Allow no more than three failed login attempts."""
    print_heading("LOGIN TO SYSTEM")
    failed_attempts = 0

    while failed_attempts < 3:
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")

        try:
            user = login_user(username, password)
        except (FileNotFoundError, RuntimeError, ConnectionError):
            print("Login is currently unavailable because the database cannot be reached.")
            return
        except Exception as error:
            print("Login could not be completed due to an unexpected error.")
            print(f"Developer details: {error}")
            return

        if user is not None:
            dashboard(user)
            return

        failed_attempts += 1
        print("Invalid username or password.")
        if failed_attempts < 3:
            print(f"Login failed.\nAttempts remaining: {3 - failed_attempts}")

    print("Maximum login attempts reached.")
    print("Returning to main menu...")


def main():
    """Run the main application menu."""
    while True:
        print_heading("USER AUTHENTICATION SYSTEM")
        print("1. Register New Account")
        print("2. Login to System")
        print("3. Exit Application")
        print("=" * 40)
        choice = input("Select an option: ").strip()

        if choice == "1":
            registration_screen()
        elif choice == "2":
            login_screen()
        elif choice == "3":
            print("Thank you for using the system.")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()