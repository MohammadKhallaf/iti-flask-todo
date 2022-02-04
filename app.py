from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType

from forms import InsertTask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'someRandomXYZkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasklist.db'
db = SQLAlchemy(app)


task_list = [{
    'id': 1,
    'title': 'somerandomtitle',
    'description': 'gerghserg',
    'status': 0,
}]


class Todo(db.Model):

    __tablename__ = 'todolist'

    types = [
        (0, 'High Priority'),
        (1, 'Mid Priority'),
        (2, 'Low Priority')
    ]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    state = db.Column(db.ChoiceType(types)) # !!?

    def __repr__(self):
        return f"{self.title}"


@app.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == 'POST':
    return render_template('home/tasks.html', tasks=task_list, form=InsertTask())


@app.route('/add', methods=['POST'])
def add():
    # form = InsertTask(request.form)
    task = {
        'id': (task_list[-1]['id'] + 1) | 0,
        'title': request.form['task_title'],
        'description': request.form['task_desc'],
        'status': int(request.form['task_status'])
    }

    task_list.append(task)
    return redirect(url_for('home'))


@app.route('/del/<int:id>')
def delete(id):
    global task_list
    task_list = list(filter(lambda item: item['id'] != id, task_list))
    # task_list.append(task)
    return redirect(url_for('home'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    req_task = {}
    if request.method == 'POST':

        uptask = {
            'id': id,
            'title': request.form['task_title'],
            'description': request.form['task_desc'],
            'status': int(request.form['task_status'])
        }
        for task in task_list:
            if task['id'] == id:
                task.update(uptask)
                break

        return redirect(url_for('home'))
    else:
        for task in task_list:
            if task['id'] == id:
                req_task = task
                break

    return render_template('home/task.html', task=req_task, form=InsertTask())


if __name__ == '__main__':
    app.run(debug=True)
