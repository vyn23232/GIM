# GIM - Membership Management System

## Overview

The **Membership Management System (GIM)** is a Django-based web application designed to streamline the management of users and their gym memberships. The system enables administrators to register users, track membership details, and manage gym class subscriptions efficiently. Users can be assigned various membership types, with automatic tracking of their membership periods. The application also allows for dynamic updates to user and membership statuses.

## Key Features
- **Admin User Management**: Admin can add, view, and manage user details, including their name, email, mobile number, and gym class subscriptions.
- **Membership Management**: Keep track of membership information, including membership plan, payment details, payment amount, payment method, payment date.
- **Dynamic Updates**: The ability to update user profiles and membership statuses in real-time, ensuring the system reflects the latest data.
- **Responsive Design**: Optimized for desktop users ensuring a seamless user experience across dekstop platforms.

## Links

- **UI/UX Design (Figma)**: [Figma Design](https://www.figma.com/design/vasctcpZrMjBhusc0ZcXgd/GMMYS-UI%2FUX?node-id=0-1&t=7iQ5nbq7QesXEvrQ-1)
- **Entity Relationship Diagram (ERD)**: [View ERD](https://drive.google.com/file/d/1dy-xeEKZtHsnG8stu4BsWxdPTAubW09s/view?usp=sharing)
- **Gantt Chart**: [View Gantt Chart](https://drive.google.com/file/d/1dy-xeEKZtHsnG8stu4BsWxdPTAubW09s/view?usp=sharing)

## Technologies Used

- **Django**: A high-level Python web framework used to build the backend of the application, providing a robust and secure platform for user and membership management.
- **HTML, CSS, JavaScript**: Front-end technologies that power the interactive, responsive user interface, ensuring the application is user-friendly and visually appealing.

## Installation & Setup

### Prerequisites

- Python 3.12.6
- Django
- DBSqlite3

### Steps to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/GIM.git
    cd GIM
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database (PostgreSQL or your chosen database):
    - Configure database settings in `settings.py`.

4. Run database migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser for admin access:
    ```bash
    python manage.py createsuperuser
    ```

6. Run the application:
    ```bash
    python manage.py runserver
    ```

7. Access the system by visiting `http://127.0.0.1:8000` in your browser.
