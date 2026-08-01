from datetime import datetime

import pytz
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from src.database.db import db

class BlacklistedToken(db.Model):
    """
    Model to store blacklisted JWT tokens
    """
    __tablename__ = 'blacklisted_token'
    __table_args__ = {'extend_existing': True}

    jti = db.Column(db.String(128), primary_key=True)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti, expires_at=None):
        self.jti = jti
        self.expires_at = expires_at or datetime.now(pytz.UTC)

    def as_dict(self):
        return {
            "jti": self.jti,
            "expires_at": self.expires_at.isoformat(),
        }

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            "username": self.username,
            "id": self.id,
            "name": self.name,
        }

