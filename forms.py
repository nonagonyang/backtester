"""Forms for Python Trader app."""
from wtforms import SelectField,DateField,StringField,PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length



class BackTestingForm(FlaskForm):
    """Form for backtesting trading strategies."""
    cash_amount=SelectField("Choose your cash amount", choices=[10000,100000,1000000])
    stock_id=SelectField("Choose a Stock", validate_choice=False,coerce=int)
    strategy_id=SelectField("Choose a Strategy", validate_choice=False,coerce=int)
    start_date=DateField("Start date",format='%Y-%m-%d')
    end_date=DateField("End date",format='%Y-%m-%d')
    note=StringField("Note")


class UserAddForm(FlaskForm):
    """Form for adding users."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])


# class UserEditForm(FlaskForm):
#     """Form for editing users."""

#     username = StringField('Username', validators=[DataRequired()])
#     email = StringField('E-mail', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
