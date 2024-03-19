from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/tasks'  
db = SQLAlchemy(app)
class IdPass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

@app.route('/')
def signin():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = IdPass.query.filter_by(username=username, password=password).first()
    if user:
        # Successful login, redirect to list.html
        return render_template('app.html')
    else:
        # Incorrect username or password, redirect back to sign-in page with a message
        return render_template('login.html', msg='Incorrect username or password.')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@app.route('/')
def landing_page():
    return render_template('app.html')

@app.route('/list')
def todo_list_page():
    return render_template('list.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [{'id': task.id, 'name': task.name} for task in tasks]
    return jsonify(task_list)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    name = data.get('name')
    if name:
        new_task = Task(name=name)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id, 'name': new_task.name}), 201
    else:
        return jsonify({'error': 'Task name is required'}), 400

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    name = data.get('name')
    task = Task.query.get(task_id)
    if task:
        task.name = name
        db.session.commit()
        return jsonify({'id': task.id, 'name': task.name}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
