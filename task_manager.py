# Import necessary libraries
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, HiddenField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'  # Database URI for SQLite
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Secret key for CSRF protection and session management
db = SQLAlchemy(app)  # Initialize SQLAlchemy with Flask app
csrf = CSRFProtect(app)  # Enable CSRF protection

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(100), nullable=False)  # Task title, cannot be null
    description = db.Column(db.Text)  # Task description, optional
    due_time = db.Column(db.DateTime, nullable=False)  # Due time, cannot be null
    completed = db.Column(db.Boolean, default=False)  # Completion status, default is False
    csrf_token = HiddenField()  # Hidden field for CSRF token

# Define the form for adding and editing tasks
class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  # Title field, required
    description = TextAreaField('Description')  # Description field, optional
    due_time = DateTimeField('Due Time', validators=[DataRequired()])  # Due time field, required

# Define route for the index page
@app.route('/')
def index():
    tasks = Task.query.all()  # Retrieve all tasks from the database
    form = TaskForm()  # Create an instance of the form class
    return render_template('index.html', tasks=tasks, form=form)  # Render the index template with tasks and form

# Define route for adding a new task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']  # Get title from form data
    description = request.form['description']  # Get description from form data
    due_time_str = request.form['datetime']  # Get due time as string from form data
    due_time = datetime.strptime(due_time_str, '%Y-%m-%dT%H:%M')  # Convert string to datetime object
    new_task = Task(title=title, description=description, due_time=due_time)  # Create a new Task instance
    db.session.add(new_task)  # Add new task to the session
    db.session.commit()  # Commit the session to the database
    return redirect(url_for('index'))  # Redirect to the index page

# Define route for editing an existing task
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)  # Retrieve task by ID or return 404 if not found
    if request.method == 'POST':
        task.title = request.form['title']  # Update title from form data
        task.description = request.form['description']  # Update description from form data
        due_time_str = request.form['datetime']  # Get due time as string from form data
        task.due_time = datetime.strptime(due_time_str, '%Y-%m-%dT%H:%M')  # Convert string to datetime object
        db.session.commit()  # Commit the changes to the database
        return redirect(url_for('index'))  # Redirect to the index page
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_time': task.due_time.strftime('%Y-%m-%dT%H:%M')  # Format datetime as string
    })  # Return task data as JSON for the GET request

# Define route for deleting a task
@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)  # Retrieve task by ID or return 404 if not found
    db.session.delete(task)  # Delete the task
    db.session.commit()  # Commit the deletion to the database
    return redirect(url_for('index'))  # Redirect to the index page

# Define route for marking a task as complete
@app.route('/complete/<int:id>', methods=['POST'])
def complete_task(id):
    task = Task.query.get_or_404(id)  # Retrieve task by ID or return 404 if not found
    task.completed = True if request.form.get('completed') == 'on' else False  # Update completion status
    db.session.commit()  # Commit the changes to the database
    return redirect('/')  # Redirect to the index page

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they do not exist
    app.run(debug=True)  # Run the Flask application in debug mode
