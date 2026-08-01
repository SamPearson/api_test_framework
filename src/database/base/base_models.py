from datetime import datetime
from typing import Any, Dict, Optional, List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from src.database.db import db



class BaseModel(db.Model):
    """
    Abstract base class for all models.
    No timestamps - simple ID-based identification for tests.
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name automatically from class name."""
        return cls.__name__.lower()

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary representation.
        Minimal - just id field.
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None

        }

class UserOwnedModel(BaseModel):
    """
    Abstract base class for models owned by a user.
    Provides user relationship and ownership validation.
    """
    __abstract__ = True

    @declared_attr
    def user_id(cls):
        return Column(Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    @declared_attr
    def user(cls):
        return db.relationship(
            'User',
            backref=db.backref(
                f'{cls.__tablename__}_list',
                cascade="all, delete-orphan"
            )
        )

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary including user_id.
        """
        data = super().as_dict()
        data['user_id'] = self.user_id
        return data

