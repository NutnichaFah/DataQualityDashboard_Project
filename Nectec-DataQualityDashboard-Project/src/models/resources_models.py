from sqlalchemy import inspect
from datetime import datetime

from .. import db # from __init__.py

class resource(db.Model): #models.py
    __tablename__ = 'resource'
    id                      = db.Column(db.String(100), primary_key=True, nullable=False, unique=True)
    url                     = db.Column(db.String(), nullable=False)
    format                  = db.Column(db.String(), nullable=False)
    description             = db.Column(db.String(), nullable=False)
    position                = db.Column(db.Integer)
    hash                    = db.Column(db.String(), nullable=False)
    state                   = db.Column(db.String(), nullable=False)
    extras                  = db.Column(db.String(), nullable=False)
    name                    = db.Column(db.String(), nullable=False)
    resource_type           = db.Column(db.String(), nullable=False)
    mimetype                = db.Column(db.String(), nullable=False)
    mimetype_inner          = db.Column(db.String(), nullable=False)
    size                    = db.Column(db.Integer)
    last_modified           = db.Column(db.DateTime(timezone=False), default=datetime.now)
    cache_url               = db.Column(db.String(), nullable=False)
    cache_last_updated      = db.Column(db.DateTime(timezone=False), default=datetime.now)
    webstore_url            = db.Column(db.String(), nullable=False)
    webstore_last_updated   = db.Column(db.DateTime(timezone=False), default=datetime.now)
    created                 = db.Column(db.DateTime(timezone=False), default=datetime.now)
    url_type                = db.Column(db.String(), nullable=False)
    package_id              = db.Column(db.String(), nullable=False)
    metadata_modified       = db.Column(db.DateTime(timezone=False), default=datetime.now)

# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
