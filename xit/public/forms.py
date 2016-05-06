from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import PasswordField, RadioField, TextField
from wtforms.validators import DataRequired


class CsvUploadForm(Form):
    xplan_url = TextField(
        'XPLAN URL',
        validators=[DataRequired()])
    xplan_username = TextField(
        'Username',
        validators=[DataRequired()])
    xplan_password = PasswordField(
        'Password',
        validators=[DataRequired()])
    csv_type = RadioField(
        'CSV Type',
        choices=(('users', 'Upload a CSV of new users'), ('access_levels', ' Upload a CSV of new and existing Access Levels')),
        default='users',
        validators=[DataRequired()])
    file = FileField('CSV File', validators=[
        DataRequired(),
        FileAllowed(
            ('csv',),
            ('Only CSV files can be uploaded for this field'))])
