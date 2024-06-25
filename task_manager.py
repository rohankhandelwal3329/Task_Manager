# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, HiddenField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CSRFProtect

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SECRET_KEY'] = 'f3df9a5888faa5795577988f938a1b83'  
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_time = db.Column(db.DateTime, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    csrf_token = HiddenField()

# Define routes
@app.route('/')
def index():
    tasks = Task.query.all()
    form = TaskForm()  # Create an instance of your form class
    return render_template('index.html', tasks=tasks, form=form)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    due_time_str = request.form['datetime']
    due_time = datetime.strptime(due_time_str, '%Y-%m-%dT%H:%M')
    new_task = Task(title=title, description=description, due_time=due_time)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        due_time_str = request.form['datetime']
        task.due_time = datetime.strptime(due_time_str, '%Y-%m-%dT%H:%M')
        db.session.commit()
        return redirect(url_for('index'))
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_time': task.due_time.strftime('%Y-%m-%dT%H:%M')  # Format datetime as string
    })

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:id>', methods=['POST'])
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = True if request.form.get('completed') == 'on' else False
    db.session.commit()
    return redirect('/')

#For editing the existing task
class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_time = DateTimeField('Due Time', validators=[DataRequired()])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
