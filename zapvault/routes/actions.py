import os
from flask import Blueprint, redirect, session
from .. import db
from ..models.file import File

actions_bp = Blueprint('actions_bp', __name__)

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
