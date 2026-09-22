# Python CLI Login and Registration System Using Microsoft Access

## Author

**CJAY I. AMORES**  
**BSIT 3-T2**

## Project Description

This is a command-line user authentication system for a Database Management
Systems practical. It uses Python, Microsoft Access, `pyodbc`, and `bcrypt` to
register users, securely verify logins, show a profile, and log users out.

The application does not create the Access database automatically. Create
`UserSystem.accdb` manually in Microsoft Access as described below.

## Features

- Register a new account with validation.
- Store passwords only as bcrypt hashes.
- Login with a maximum of three failed attempts.
- Use one generic message for an unknown username or incorrect password.
- Show a personalized dashboard using the name stored in the database.
- View a profile without showing password or password-hash data.
- Logout and return to the main menu.
- Check the Access ODBC driver and database connection.

## Technologies Used

- Python 3
- Microsoft Access (`.accdb`)
- `pyodbc`
- `bcrypt`
- Command Line Interface (CLI)

## Project Structure

```text
DBMS_Login_System/
|-- main.py
|-- database.py
|-- auth.py
|-- requirements.txt
|-- README.md
|-- .gitignore
`-- UserSystem.accdb   (created manually and ignored by Git)
```

## Installation

Open PowerShell in this project folder and run:

```powershell
python -m pip install --upgrade pip
python -m pip install pyodbc bcrypt
```

You can also install from the requirements file:

```powershell
python -m pip install -r requirements.txt
```

## Required Python Packages

`requirements.txt` contains:

```text
pyodbc
bcrypt
```

## Microsoft Access Database Setup

1. Open Microsoft Access.
2. Create a blank database named `UserSystem.accdb`.
3. Save it directly inside this project folder, beside `main.py`.
4. Create a table named `Users` in Design View.
5. Add these fields:

| Field Name | Data Type | Required settings |
| --- | --- | --- |
| `UserID` | AutoNumber | Primary Key |
| `FullName` | Short Text | Field Size `100`, Required `Yes` |
| `Username` | Short Text | Field Size `50`, Required `Yes`, Indexed `Yes (No Duplicates)` |
| `PasswordHash` | Short Text | Field Size `255`, Required `Yes` |
| `Email` | Short Text | Field Size `100`, Required `Yes` |
| `DateRegistered` | Date/Time | Required `Yes`, Default Value `Now()` |

6. Save the table as `Users`.
7. Confirm that `UserID` is the primary key and `Username` has no duplicate
   index.

Never add plaintext passwords to the table. The `PasswordHash` field must
contain only bcrypt hashes produced by the application.

## Test the Database Connection

After the database and `Users` table exist, run:

```powershell
python database.py
```

Expected output resembles:

```text
Database connected successfully!
Total users in database: 0
```

## Run the Application

```powershell
python main.py
```

Choose `1` to register, `2` to log in, or `3` to exit. Password prompts use
`getpass`, so typed passwords are hidden.

## Login and Registration Flow

Registration asks for full name, username, password, password confirmation,
and email. It checks required fields, username length and uniqueness, password
length and confirmation, and a basic email format.

Login asks for a username and hidden password. Three failed attempts are
allowed. A successful login opens the dashboard, where the user can view the
profile or logout back to the main menu.

## Security Features

- Passwords are hashed with `bcrypt.gensalt(rounds=12)`.
- Passwords are checked with `bcrypt.checkpw()`.
- Password hashes are never returned in dashboard or profile data.
- User input is passed through parameterized SQL queries using `?` placeholders.
- Unknown usernames and incorrect passwords use the same generic error message.
- The Access database file is excluded from Git by `.gitignore`.

## Testing Checklist

- [ ] TC-01: Register with valid details.
- [ ] TC-02: Register with a duplicate username.
- [ ] TC-03: Register with an empty full name.
- [ ] TC-04: Register with mismatched passwords.
- [ ] TC-05: Login with correct credentials.
- [ ] TC-06: Login with an incorrect password.
- [ ] TC-07: Login with a nonexistent username.
- [ ] TC-08: Fail login three times and confirm return to the main menu.
- [ ] TC-09: View profile and confirm no password information appears.
- [ ] TC-10: Logout and confirm the main menu appears.

## Troubleshooting

### Database file not found

Make sure `UserSystem.accdb` is in the same folder as `main.py`, and make sure
the filename is spelled exactly as shown.

### Access driver unavailable

Install the Microsoft Access Database Engine / Access ODBC driver. Python and
the driver must have matching architecture: both 32-bit or both 64-bit.

The application checks for this exact driver name:

```text
Microsoft Access Driver (*.mdb, *.accdb)
```

### Users table errors

Confirm that the table is named `Users` and that all field names, required
settings, data types, and field sizes match the setup table above.

### Package import errors

Run the installation commands again using the same Python interpreter used to
run the application:

```powershell
python -m pip install pyodbc bcrypt
```

### Architecture mismatch

If `pyodbc` cannot load the Access driver, check whether your Python
installation is 32-bit or 64-bit and install the matching Access Database
Engine version.# Python CLI Login and Registration System Using Microsoft Access

## Project Description

This project is a command-line login and registration system for a Database Management Systems practical. It stores user accounts in a Microsoft Access `.accdb` database and protects passwords with bcrypt hashes.

## Features

- Register a new account from the command line
- Validate names, usernames, passwords, confirmation passwords, and email addresses
- Prevent duplicate usernames
- Login with a maximum of three failed attempts
- Display a personalized dashboard using the user's database record
- View a profile without displaying password information
- Logout and return to the main menu
- Use parameterized SQL queries for user input

## Technologies Used

- Python 3
- Microsoft Access (`.accdb`)
- `pyodbc`
- `bcrypt`
- Command Line Interface (CLI)

## Project Structure

```text
DBMS_Login_System/
├── main.py
├── database.py
├── auth.py
├── requirements.txt
├── README.md
├── .gitignore
└── UserSystem.accdb        # Create this manually in Microsoft Access
```

## Installation

Open PowerShell in this project folder and run:

```powershell
python -m pip install --upgrade pip
python -m pip install pyodbc bcrypt
```

The required Python packages are also listed in `requirements.txt`.

## Microsoft Access Database Setup

The program does not create a fake database file. Create `UserSystem.accdb` manually in Microsoft Access:

1. Open Microsoft Access.
2. Choose **Blank database**.
3. Name the file `UserSystem.accdb`.
4. Save it directly inside the `DBMS_Login_System` project folder.
5. Create a table named `Users` in **Design View**.
6. Add the fields below.

| Field Name | Data Type | Required / Other Settings |
|---|---|---|
| `UserID` | AutoNumber | Primary Key |
| `FullName` | Short Text | Field Size 100; Required Yes |
| `Username` | Short Text | Field Size 50; Required Yes; Indexed: Yes (No Duplicates) |
| `PasswordHash` | Short Text | Field Size 255; Required Yes |
| `Email` | Short Text | Field Size 100; Required Yes |
| `DateRegistered` | Date/Time | Required Yes; Default Value `Now()` |

Save the table as `Users`. Never create a plaintext password field or manually enter plaintext passwords into `PasswordHash`. The application stores only bcrypt hashes.

## Test the Database Connection

After creating the database and table, run:

```powershell
python database.py
```

Successful output includes:

```text
Database connected successfully!
Total users in database: 0
```

## Run the Application

```powershell
python main.py
```

## Login and Registration Flow

1. Select **Register New Account**.
2. Enter the full name, username, hidden password, confirmation password, and email.
3. After successful registration, select **Login to System**.
4. Enter the username and hidden password.
5. A successful login opens the personalized dashboard.
6. Select **View Profile** to see safe account details.
7. Select **Logout** to return to the main menu.

For both an unknown username and an incorrect password, the application displays the same message: `Invalid username or password.`

## Security Features

- Passwords are entered with `getpass.getpass()` and are hidden while typing.
- Passwords are hashed with `bcrypt.gensalt(rounds=12)`.
- Password verification uses `bcrypt.checkpw()`.
- Plaintext passwords and password hashes are not returned to the dashboard or profile.
- User input is passed through parameterized SQL queries using `?` placeholders.
- Login attempts are limited to three failures.
- The Access database is excluded from Git with `.gitignore`.

## Testing Checklist

- [ ] TC-01: Register with valid details.
- [ ] TC-02: Register again with the same username.
- [ ] TC-03: Register with an empty full name.
- [ ] TC-04: Enter different password and confirmation values.
- [ ] TC-05: Login with correct credentials.
- [ ] TC-06: Login with an incorrect password.
- [ ] TC-07: Login with a nonexistent username.
- [ ] TC-08: Fail login three times and confirm return to the main menu.
- [ ] TC-09: View the profile and confirm no password or password hash appears.
- [ ] TC-10: Logout and confirm the main menu is displayed.

## Troubleshooting

### Database file not found

Confirm that `UserSystem.accdb` is saved directly beside `main.py` and `database.py`, not in a subfolder.

### Access driver unavailable

Install the Microsoft Access Database Engine / Access ODBC driver. Python and the Access driver must have matching 32-bit or 64-bit architecture. The required driver name is:

```text
Microsoft Access Driver (*.mdb, *.accdb)
```

### Users table error

Confirm that the table is named `Users` and that every field name, data type, required setting, index, and default value matches the table above.

### Python package error

Run the installation commands again in the same Python environment used to run the program:

```powershell
python -m pip install pyodbc bcrypt
```

### Database is locked

Close `UserSystem.accdb` in Microsoft Access while running the Python application. Also close any stale Access lock file before trying again.