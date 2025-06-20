import os
from flask import Blueprint, send_from_directory, redirect, session
from .. import db
from ..models.file import File
from ..utils.helpers import IST
from datetime import datetime
import pytz

actions_bp = Blueprint('actions_bp', __name__)

@actions_bp.route('/download/<file_id>')
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
    return send_from_directory("uploads", file_record.filename, as_attachment=True)


@actions_bp.route('/expire/<file_id>')
def expire_file(file_id):
    if 'user' not in session:
        return redirect('/login')

    file_record = File.query.filter_by(id=file_id).first()
    if file_record:
        file_record.expired = True
        db.session.commit()
    return redirect('/dashboard')


@actions_bp.route('/delete/<file_id>')
def delete_file(file_id):
    if 'user' not in session:
        return redirect('/login')

    file = File.query.get(file_id)
    if file:
        try:
            os.remove(os.path.join("uploads", file.filename))
        except:
            pass
        db.session.delete(file)
        db.session.commit()
    return redirect('/dashboard')
