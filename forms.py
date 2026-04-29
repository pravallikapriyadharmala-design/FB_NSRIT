from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('student', 'Student'), ('admin', 'Admin')], default='student')
    roll_number = StringField('Roll Number (Student only)', default='')
    name = StringField('Full Name (Student only)', default='')
    branch = SelectField('Branch (Student only)', choices=[
        ('', 'Select Branch'),
        ('CSE', 'Computer Science & Engineering'),
        ('CSE-AI&ML', 'CSE - AI & Machine Learning'),
        ('CSE-DS', 'CSE - Data Science'),
        ('ECE', 'Electronics & Communication'),
        ('EEE', 'Electrical & Electronics'),
        ('Mechanical', 'Mechanical Engineering'),
        ('Civil', 'Civil Engineering')
    ], default='')
    semester = SelectField('Semester (Student only)', choices=[
        ('', 'Select Semester'),
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
        ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8')
    ], default='')
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
