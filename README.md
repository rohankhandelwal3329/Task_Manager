# Task Manager

A simple web-based task manager application built with Flask and SQLite.

# Features:

- Add, edit, and delete tasks
- Mark tasks as complete or incomplete
- View all tasks in a table
- CSRF protection with Flask-WTF

# Requirements:

- Python 3.6+
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- python-dotenv

# Installation:
# 1. Clone the repository:
- git clone https://github.com/rohankhandelwal3329/task_manager.git
- cd task-manager

# 2. Install the dependencies:
- pip install -r requirements.txt

# 3. Create a .env file in the root directory and add your secret key:
- SECRET_KEY=your_secret_key

# 4. Initialize the database:
- flask db init
- flask db migrate
- flask db upgrade

# Usage:
# 1. Run the Flask application:
- flask run
- Open your web browser and go to http://127.0.0.1:5000.


# File Structure:
- task_manager.py: Main application file containing the Flask application and routes.
- templates/index.html: HTML template for the task manager interface.
- requirements.txt: List of Python dependencies.

# Routes:
- /: Displays the task manager interface with the list of tasks.
- /add: Adds a new task. Accepts POST requests.
- /edit/<int:task_id>: Edits an existing task. Accepts GET and POST requests.
- /delete/<int:id>: Deletes a task.
- /complete/<int:id>: Marks a task as complete or incomplete.
