from email.policy import default

from numpy.ma.extras import unique
from sqlalchemy import union
from sqlalchemy.ext.hybrid import hybrid_property
from db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer)
    uid = db.Column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # @hybrid_property
    # def password(self):
    #     return self._password
    #
    # @password.setter
    # def password(self, value):
    #     self._password = pwd_contex.hash(value)
    #
    #
    # def __repr__(self):
    #     return f'<User {self.uid}: {self.name}>'