import os
from datetime import datetime
from flask import Blueprint, send_from_directory

from .. import db, app
from ..models.file import File

download_bp = Blueprint('download_bp', __name__)

@download_bp.route('/download/<file_id>')
def download_file(file_id):
    file_record = File.query.filter_by(id=file_id).first()

    if not file_record:
        return '<h3>⚠️ File not found.</h3><a href="/">Home</a>'

    if file_record.expires_at and datetime.utcnow() > file_record.expires_at:
        file_record.expired = True
        db.session.commit()
        return '<h3>⏰ Link has expired.</h3><a href="/">Home</a>'

    file_record.download_count += 1
    db.session.commit()
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_record.filename, as_attachment=True)
