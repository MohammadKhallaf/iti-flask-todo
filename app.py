"""
TODO LIST CRUD App using flask
flask_sqlalchemy    => DB interaction
sqlalchemy_utils    => ChoiceType

scenario
register -> login
all can view
users only full CRUD functions
"""
from flask import Flask, request

app = Flask(__name__)

from models import User, Todo, db

# adding jwt to auth.
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required

app.config['SECRET_KEY'] = 'someRandomXYZkey'

# Initiate JWT
app.config['JWT_SECRET_KEY'] = 'someRandomXYZ#jwtkey'
jwt = JWTManager(app)


@app.before_first_request
def create_table():
    db.create_all()


''' lab1 - list of dictionaries to save data 
task_list = [{
    'id': 1,
    'title': 'somerandomtitle',
    'description': 'gerghserg',
    'status': 0,
}]
'''

"""
Creating functions to routes
"""


@app.route('/', methods=['GET', 'POST'])
def home():
    task_list = Todo.query.all()
    json_list = []
    for item in task_list:
        json_list.append({'title': item.title,
                          'desc': item.description,
                          'stat': item.status.code})
    print(json_list)
    return {'data': json_list}


""" return render_template('home/tasks.html', tasks=task_list, form=InsertTask())"""


@app.route('/add', methods=['POST'])
@jwt_required()
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
    """ lab-2
    
    task = {
        'title': request.form['task_title'],
        'description': request.form['task_desc'],
        'status': request.form['task_status']
    }
    """
    task = {
        'title': request.json.get('data').get('title'),
        'description': request.json.get('data').get('description'),
        'status': request.json.get('data').get('status'),
    }
    print(task['status'])
    new_task = Todo(title=task['title'], description=task['description'], status=task['status'])
    try:
        db.session.add(new_task)
        db.session.commit()
        return {
            "msg": "Done"
        }

        # return redirect(url_for('home')) #=> lab-2
    except:
        return "Error!"


@app.route('/del/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    ''' lab-1
        global task_list
        task_list = list(filter(lambda item: item['id'] != id, task_list))
        # task_list.append(task)
    '''
    # just delete
    task_to_del = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_del)
        db.session.commit()
    except:
        return "Error!"
    # return redirect(url_for('home')) => lab-2
    return {
        "msg": "Done"
    }


@app.route('/update/<int:pk>', methods=['PUT'])
@jwt_required()
def update(pk):
    # req_task = {}
    task_to_update = Todo.query.get_or_404(pk)
    """ lab-2
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
        """
    uptask = {
        'title': request.json.get('data').get('title'),
        'description': request.json.get('data').get('description'),
        'status': int(request.json.get('data').get('status')),
    }
    task_to_update.title = uptask['title']
    task_to_update.description = uptask['description']
    task_to_update.status = uptask['status']

    try:
        db.session.commit()
    except:
        return "Error!"

    return {'msg': "Done"}

    """ lab-2
    return redirect(url_for('home'))
    
    return render_template('home/task.html', task=task_to_update, form=InsertTask())"""


'''<------------{ lab 3 }------------>'''
''' lab3 - add authentications
- Only users can edit 
- All can View
'''


# LOGIN route
# JWT token return
@app.route('/login', methods=['POST'])
def login():
    '''
    # if it were to read from form
    username = request.form['user_name']
    password = request.form['user_pass']
    '''
    #
    # get the credits
    username = request.json.get('data').get("username")
    password = request.json.get('data').get("password")
    # user query
    user = User.query.filter_by(name=username).first()

    # checkup
    if user is not None and password == user.password:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return {"status": "success",
                "data": {
                    "msg": "Welcome in the site",
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }}

    return {
        'status': 'failed',
        'data': {
            "msg": "Bad username or password"
        }
    }


@app.route('/register', methods=['POST'])
def register():
    '''
        # if it were to read from form
        username = request.form['user_name']
        password = request.form['user_pass']
        '''
    #
    # get the credits
    username = request.json.get('data').get("username")
    password = request.json.get('data').get("password")
    # user query
    user = User.query.filter_by(name=username).first()

    # checkup if exist
    if user is not None:

        return {'status': 'failed',
                'data': {
                    "msg": "User already exists"
                }
                }
    else:
        # if not exists
        new_user = User(name=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return {"status": "success",
                    "data": {
                        "msg": "Successfully registered",

                    }
                    }
        except:
            # database commit fail
            return {"status": "fail",
                    "data": {
                        "msg": "Failed",

                    }
                    }


# TODO : !front end->clear?
@app.route('/logout', methods=['POST'])
def logout():
    return {"status": "success",
            "data": {
                "msg": "Bye !",
                'access_token': '',

            }
            }


if __name__ == '__main__':
    app.run(debug=True)
