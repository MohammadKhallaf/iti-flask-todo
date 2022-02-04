from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import ChoiceType

from forms import InsertTask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'someRandomXYZkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasklist.db'
db = SQLAlchemy(app)

'''
task_list = [{
    'id': 1,
    'title': 'somerandomtitle',
    'description': 'gerghserg',
    'status': 0,
}]
'''


@app.before_first_request
def create_table():
    db.create_all()


class Todo(db.Model):
    __tablename__ = 'todolist'

    types = [
        ('0', 'High Priority'),
        ('1', 'Mid Priority'),
        ('2', 'Low Priority')
    ]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    status = db.Column(ChoiceType(types))  # !!?

    def __repr__(self):
        return '<Todo %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def home():
    task_list = Todo.query.all()
    return render_template('home/tasks.html', tasks=task_list, form=InsertTask())


@app.route('/add', methods=['POST'])
def add():
    """ lab-1
    task = {
        'id': (task_list[-1]['id'] + 1) | 0,
        'title': request.form['task_title'],
        'description': request.form['task_desc'],
        'status': int(request.form['task_status'])
    }
    task_list.append(task)
    """
    task = {
        'title': request.form['task_title'],
        'description': request.form['task_desc'],
        'status': request.form['task_status']
    }
    new_task = Todo(title=task['title'], description=task['description'], status=task['status'])
    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    except:
        return "Error!"


@app.route('/del/<int:id>')
def delete(id):
    ''' lab-1
        global task_list
        task_list = list(filter(lambda item: item['id'] != id, task_list))
        # task_list.append(task)
    '''
    task_to_del = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_del)
        db.session.commit()
    except:
        return "Error!"
    return redirect(url_for('home'))


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    req_task = {}
    task_to_update = Todo.query.get_or_404(id)
    if request.method == 'POST':

        uptask = {
            'title': request.form['task_title'],
            'description': request.form['task_desc'],
            'status': int(request.form['task_status'])
        }
        '''
        for task in task_list:
            if task['id'] == id:
                task.update(uptask)
                break
        '''
        task_to_update.title = uptask['title']
        task_to_update.description = uptask['description']
        task_to_update.status = uptask['status']

        try:
            db.session.commit()
        except:
            return "Error!"
        return redirect(url_for('home'))

    return render_template('home/task.html', task=task_to_update, form=InsertTask())


if __name__ == '__main__':
    app.run(debug=True)
