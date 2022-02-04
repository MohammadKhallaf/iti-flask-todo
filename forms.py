from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField


class InsertTask(FlaskForm):
    task_title = StringField('Title')
    task_desc = StringField('Description')
    task_status = SelectField('Task Status', choices=[
        (0, 'High Priority'),
        (1, 'Mid Priority'),
        (2, 'Low Priority')
    ])
    submit = SubmitField('Submit')

