import os
from datetime import datetime
from flask import Blueprint, send_from_directory, current_app
from .. import db
from ..models.file import File

download_bp = Blueprint('download_bp', __name__)

@download_bp.route('/download/<file_id>')
def download_file(file_id):
    print("✅ Download route hit with file_id:", file_id)

    # ✅ TEMP DEBUG LINE
    print("📂 All files in DB:", File.query.all())
    print("🧾 All file IDs in DB:", [f.id for f in File.query.all()])


    file_record = File.query.filter_by(id=file_id).first()
    print("📦 DB file found:", file_record)

    if not file_record:
        return '<h3>⚠️ File not found.</h3><a href="/">Home</a>'

    print("🗂 File path:", os.path.join(current_app.config['UPLOAD_FOLDER'], file_record.filename))

    if file_record.expires_at and datetime.utcnow() > file_record.expires_at:
        file_record.expired = True
        db.session.commit()
        return '<h3>⏰ Link has expired.</h3><a href="/">Home</a>'

    file_record.download_count += 1
    db.session.commit()

    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        file_record.filename,
        as_attachment=True
    )

# ✅ Test route to confirm blueprint is working
@download_bp.route('/test-download')
def test_download():
    return '✅ Download blueprint is active!'
