from sqlalchemy import inspect
from datetime import datetime


from .. import db # from __init__.py

class member(db.Model): #models.py
    __tablename__ = 'member' #matches the name of the actual database table
    id                  = db.Column(db.String(100), primary_key=True, nullable=False, unique=True)
    group_id            = db.Column(db.String(), nullable=False)
    table_id            = db.Column(db.String(), nullable=False)
    state               = db.Column(db.String(), nullable=False)
    table_name          = db.Column(db.String(), nullable=False)
    capacity            = db.Column(db.String(), nullable=False)

# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }