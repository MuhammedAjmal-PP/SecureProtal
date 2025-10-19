
# Secure Portal - Custom Admin & User Management

## 📝 Project Description

This Django project implements a **Secure Portal** with a dedicated, custom-built administrative interface for managing user accounts. It replaces the default Django admin interface for user management, offering enhanced features like multi-field search, pagination, detailed profile views, and a secure CRUD (Create, Read, Update, Delete) workflow.

## ✨ Key Features

The custom admin portal includes the following functionalities:

### User Management (`/controlpanel/users/`)

  * **CRUD Operations:** Full capability to **C**reate, **R**ead (Profile View), **U**pdate (Edit), and **D**elete user accounts.
  * **Security Checks:** Implemented checks to prevent an admin from deleting their own account or a Superuser account.
  * **Detailed Profile View:** A dedicated page to view all user details, roles, and status, with direct links for editing and deletion.

### Data Handling & Presentation

  * **Pagination:** Displays only **30 users** per page to improve performance and readability.
  * **Search Functionality:** Powerful, case-insensitive search across `username`, `email`, `first_name`, and `last_name` using Django's `Q` objects.
  * **Filtering & Sorting:** Users list can be ordered/sorted by `username`, `email`, `date_joined`, and `last_login`.
  * **Status Indicators:** Visual badges indicate user status (Active/Inactive) and roles (Admin/Staff).

### Security & Sessions

  * **Secure Sessions:** Uses Django's secure, HTTP-only cookies to persist user sessions.
  * **Session Timeout:** Configured for secure session expiration based on inactivity (time value set in `settings.py`).
  * **Authentication:** Dedicated login/logout views for the admin portal.

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1\. Prerequisites

  * Python 3.8+
  * pip (Python package installer)

### 2\. Installation

1.  **Clone the Repository (if applicable):**

    ```bash
    git clone https://github.com/MuhammedAjmal-PP/SecureProtal.git
    cd SecurePortal
    ```

2.  **Create a Virtual Environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    # .venv\Scripts\activate.bat  # On Windows
    ```

3.  **Install Dependencies:**
    (You'll need `Django` and any other required libraries like `Pillow` or `psycopg2` if used.)

    ```bash
    pip install Django==5.2.7
    # or install from a requirements.txt file
    # pip install -r requirements.txt
    ```

### 3\. Database Setup

1.  **Apply Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

2.  **Create an Admin Account (Superuser):**
    You need a Superuser to access the custom admin portal.

    ```bash
    python manage.py createsuperuser
    ```

### 4\. Run the Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

-----

## 🛠️ Usage & Key URLs

### Admin Portal Endpoints

| Feature | URL | URL Name (for `{% url %}` tag) |
| :--- | :--- | :--- |
| **Admin Login** | `/controlpanel/login/` | `admin_login` |
| **Admin Logout** | `/controlpanel/logout/` | `admin_logout` |
| **User List (Management)** | `/controlpanel/users/` | `users` |
| **Add New User** | `/controlpanel/users/add/` | `add_user` |
| **View/Profile** | `/controlpanel/users/<pk>/` | `profile` |
| **Edit User** | `/controlpanel/users/edit/<pk>/` | `user_edit` |
| **Delete User** | `/controlpanel/users/<pk>/delete/` | `user_delete` |

-----

## ⚙️ Configuration Notes

### 1\. Session Settings (`settings.py`)

To adjust session behavior, modify the following variables:

```python
# settings.py

# Session expires after 30 minutes of inactivity
SESSION_COOKIE_AGE = 1800 

# Resets the countdown timer (SESSION_COOKIE_AGE) on every request
SESSION_SAVE_EVERY_REQUEST = True 

# Recommended for production over HTTPS
# SESSION_COOKIE_SECURE = True 
```

### 2\. User Forms (`custom_admin/forms.py`)

The project uses two custom forms for robust administration:

  * `AdminUserCreationForm`: Used for creating new users, includes password fields and permission settings.
  * `AdminUserChangeForm`: Used for editing existing users, excludes password fields for security.

### 3\. Pagination Limit (`custom_admin/views.py`)

To change the number of users shown per page (currently 30), modify the `Paginator` line in the `admin_users` view:

```python
# custom_admin/views.py - inside admin_users function
paginator = Paginator(users, 30) # Change 30 to your desired limit
```
