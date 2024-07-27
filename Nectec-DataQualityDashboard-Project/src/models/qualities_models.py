from sqlalchemy import inspect
from datetime import datetime

from .. import db # from __init__.py

class Data_quality_metrics(db.Model): #models.py
    __tablename__ = 'data_quality_metrics'
    id                      = db.Column(db.String(100), primary_key=True, nullable=False, unique=True)
    created_at              = db.Column(db.DateTime(timezone=True), default=datetime.now)
    modified_at             = db.Column(db.DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    type                    = db.Column(db.String(), nullable=False)
    ref_id                  = db.Column(db.String(), nullable=False)
    resource_last_modified  = db.Column(db.DateTime(timezone=True))
    timeliness              = db.Column(db.Float(), nullable=False)
    validity                = db.Column(db.Float(), nullable=False)
    consistency             = db.Column(db.Float(), nullable=False)
    openness                = db.Column(db.Float(), nullable=False)
    downloadable            = db.Column(db.Float(), nullable=False)
    access_api              = db.Column(db.Float(), nullable=False)
    machine_readable        = db.Column(db.Float(), nullable=False)
    file_size               = db.Column(db.Float(), nullable=False)
    execute_time            = db.Column(db.Float(), nullable=False)
    filepath                = db.Column(db.String(), nullable=False)
    url                     = db.Column(db.String(), nullable=False)
    metrics                 = db.Column(db.JSON)

# How to serialize SqlAlchemy PostgreSQL Query to JSON => https://stackoverflow.com/a/46180522
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    