from flask import Blueprint, session, redirect

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')