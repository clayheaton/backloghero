"""
Data models for SQLAlchemy for the app.
"""
from backloghero.database import Base
from flask_security import UserMixin, RoleMixin
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey

class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))

class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values
    # for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception
    # TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)

class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    steam_name = Column(String(80))
    steam_id = Column(Integer(), unique=True) # Add Steam Key for people with private accts?
    steam_url = Column(String(255), unique=True)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())

    # User registers but admin has to activate before they can use the site
    activated = Column(Boolean(), default=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    messages = relationship('Message', secondary='messages_users',
                            backref=backref('users'), lazy='dynamic',
                            cascade='all,delete')

# The purpose of this class is to store messages that are produced
# during background tasks and are related
# to the account of the user and not to the data under analysis.
class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    message_type = Column(String(80))
    message = Column(String(255))
    link = Column(String(80))
    link_text = Column(String(80))
    read = Column(Boolean(), default=False)

    def __str__(self):
        return self.message

    def __hash__(self):
        return hash(self.message)
