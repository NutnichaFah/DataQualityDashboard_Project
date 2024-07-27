from sqlalchemy import inspect
from datetime import datetime


from .. import db # from __init__.py

class group(db.Model): #models.py
    __tablename__ = 'group' #matches the name of the actual database table
    id                = db.Column(db.String(100), primary_key=True, nullable=False, unique=True)
    name              = db.Column(db.String(), nullable=False)
    title             = db.Column(db.String(), nullable=False)
    description       = db.Column(db.String(100), nullable=False)
    created           = db.Column(db.DateTime(timezone=False), default=datetime.now)
    state             = db.Column(db.String(), nullable=False)
    type              = db.Column(db.String(), nullable=False)
    approval_status   = db.Column(db.String(), nullable=False)
    image_url         = db.Column(db.String(), nullable=False)
    is_organization   = db.Column(db.Boolean, nullable=False)

# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }