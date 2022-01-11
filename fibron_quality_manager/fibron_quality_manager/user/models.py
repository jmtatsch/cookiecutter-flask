# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from fibron_quality_manager.database import Column, PkModel, db, reference_col, relationship
from fibron_quality_manager.extensions import bcrypt


class Role(PkModel):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col("users", nullable=True)
    user = relationship("User", backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(UserMixin, PkModel):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    _password = Column("password", db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    @hybrid_property
    def password(self):
        """Hashed password."""
        return self._password

    @password.setter
    def password(self, value):
        """Set password."""
        self._password = bcrypt.generate_password_hash(value)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self._password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.username!r})>"


class Job(PkModel):
    """A production job for production of pipes."""

    __tablename__ = "jobs"
    name = Column(db.String(80), unique=True, nullable=False)
    creator_user_id = reference_col("users", nullable=True)
    creator_user = relationship("User", backref="job")

    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    product_type = Column(db.String(80), nullable=True)
    product_length = Column(db.Float(), nullable=True)
    product_diameter = Column(db.Float(), nullable=True)
    product_layers = Column(db.Integer(), nullable=True)

    production_started_at = Column(db.DateTime, nullable=True)
    production_finished_at = Column(db.DateTime, nullable=True)


    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"

class Spool(PkModel):
    """A spool can contain fresh or processed pipe."""

    __tablename__ = "spools"
    description = Column(db.String(80))
    empty = Column(db.Boolean(), default=True)

    def __init__(self, description, **kwargs):
        """Create instance."""
        super().__init__(description=description, **kwargs)



class Customer(PkModel):
    """A customer."""
    __tablename__ = "customers"
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    company_name = Column(db.String(30), nullable=True)

    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    email = Column(db.String(80), unique=True, nullable=False)

    active = Column(db.Boolean(), default=False)