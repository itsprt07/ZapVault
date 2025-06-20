from .. import db
from datetime import datetime

class File(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    expired = db.Column(db.Boolean, default=False)
    download_count = db.Column(db.Integer, default=0)
    token = db.Column(db.String(6), nullable=False)
