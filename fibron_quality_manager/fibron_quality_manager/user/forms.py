# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User, Job, Spool, Customer


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField("Verify password", [DataRequired(), EqualTo("password", message="Passwords must match")],)

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append("Username already registered")
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already registered")
            return False
        return True

class NewJobForm(FlaskForm):
    """New Job form."""

    name = StringField("Jobname", validators=[DataRequired(), Length(min=3, max=25)])
    product_type = StringField("Product type", validators=[DataRequired(), Length(min=1, max=25)])
    product_length = StringField("Product length", validators=[DataRequired(), Length(min=1, max=40)])
    product_diameter = StringField("Product diameter", validators=[DataRequired(), Length(min=1, max=3)])
    product_layers = StringField("Product layers", validators=[DataRequired(), Length(min=1, max=2)])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(NewJobForm, self).__init__(*args, **kwargs)
        self.user = None
    
    def validate(self):
        """Validate the form."""
        initial_validation = super(NewJobForm, self).validate()
        if not initial_validation:
            return False
        name = Job.query.filter_by(name=self.name.data).first()
        if name:
            self.name.errors.append("Name already exists")
            return False
        return True

class NewSpoolForm(FlaskForm):
    """New spool form."""

    description = StringField("Spool Description", validators=[DataRequired(), Length(min=3, max=25)])
    
    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(NewSpoolForm, self).__init__(*args, **kwargs)
    
    def validate(self):
        """Validate the form."""
        initial_validation = super(NewSpoolForm, self).validate()
        if not initial_validation:
            return False
        else:
            return True