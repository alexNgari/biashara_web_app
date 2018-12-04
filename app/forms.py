from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length

class RegisterBusinessForm(FlaskForm):
    categories = [('Tech', 'Technology'), ('Craft', 'Craft'), ('Ent', 'Entertainment'), ('Service', 'Service'), ('Agriculture', 'Agriculture')]
    name = StringField('Business name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=categories)
    description = SelectField('Description', validators=[DataRequired])