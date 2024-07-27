from sqlalchemy import inspect
from datetime import datetime


from .. import db # from __init__.py

class package(db.Model): #models.py
    __tablename__ = 'package' #matches the name of the actual database table
    id                = db.Column(db.String(100), primary_key=True, nullable=False, unique=True)
    name              = db.Column(db.String(), nullable=False)
    title             = db.Column(db.String(), nullable=False)
    version           = db.Column(db.String(100), nullable=False)
    url               = db.Column(db.String(), nullable=False)
    notes             = db.Column(db.String(), nullable=False)
    author            = db.Column(db.String(), nullable=False)
    author_email      = db.Column(db.String(), nullable=False)
    maintainer        = db.Column(db.String(), nullable=False)
    maintainer_email  = db.Column(db.String(), nullable=False)
    state             = db.Column(db.String(), nullable=False)
    license_id        = db.Column(db.String(), nullable=False)
    type              = db.Column(db.String(), nullable=False)
    owner_org         = db.Column(db.String(), nullable=False)
    private           = db.Column(db.Boolean(), nullable=False)
    metadata_modified = db.Column(db.DateTime(timezone=False), default=datetime.now)
    creator_user_id   = db.Column(db.String(100), nullable=False)
    metadata_created  = db.Column(db.DateTime ,nullable=False, default=datetime.now)

# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }