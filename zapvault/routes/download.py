import os
from datetime import datetime
from flask import Blueprint, send_file, current_app, abort
from .. import db
from ..models.file import File

download_bp = Blueprint('download_bp', __name__)

@download_bp.route('/download/<file_id>')
def download_file(file_id):
    print("✅ Download route hit with file_id:", file_id)

    file_record = File.query.filter_by(id=file_id).first()
    print("📦 DB file found:", file_record)

    if not file_record:
        abort(404)

    # Check expiry
    if file_record.expires_at and datetime.utcnow() > file_record.expires_at:
        file_record.expired = True
        db.session.commit()
        abort(403)

    # Increment download count
    file_record.download_count += 1
    db.session.commit()

    # Send file directly with no redirect or page
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_record.filename)

    if not os.path.exists(full_path):
        abort(404)

    return send_file(
        full_path,
        as_attachment=True,
        download_name=file_record.filename,
        mimetype='application/octet-stream'
    )
