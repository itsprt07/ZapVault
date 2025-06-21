from flask import Blueprint, session, redirect, url_for
from ..models.user import User
from ..models.file import File
from .. import db
from ..utils.helpers import IST

from datetime import datetime
import pytz  # ✅ Import this to handle timezone conversion

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard():
    if 'user' not in session:
        return redirect('/')

    user = User.query.filter_by(email=session['user']).first()
    if not user:
        return redirect('/')

    files = File.query.filter_by(token=user.token).order_by(File.timestamp.desc()).all()

    total_files = len(files)
    total_downloads = sum(f.download_count for f in files)
    expired_files = sum(1 for f in files if f.expired or datetime.utcnow() > f.expires_at)
    last_upload = max((f.timestamp for f in files), default=None)
    last_upload_str = last_upload.replace(tzinfo=pytz.UTC).astimezone(IST).strftime('%Y-%m-%d %I:%M:%S %p') if last_upload else "No uploads yet"

    rows = ""
    for f in files:
        # ✅ Proper UTC → IST conversion
        ist_uploaded = f.timestamp.replace(tzinfo=pytz.UTC).astimezone(IST)
        ist_expiry = f.expires_at.replace(tzinfo=pytz.UTC).astimezone(IST)
        is_expired = datetime.utcnow() > f.expires_at
        status = "❌ Expired" if is_expired or f.expired else "✅ Active"

        rows += f'''
        <tr>
            <td><div class="filename-cell">{f.filename}</div></td>
            <td>{ist_uploaded.strftime('%Y-%m-%d %I:%M:%S %p')}</td>
            <td>{ist_expiry.strftime('%Y-%m-%d %I:%M:%S %p')}</td>
            <td>{f.download_count}</td>
            <td>{status}</td>
            <td class="action-cell">
                <a class="action-btn download" href="{url_for('download_bp.download_file', file_id=f.id)}">⬇️ Download</a>
                <a class="action-btn delete" href="/delete/{f.id}">🗑️ Delete</a>
                <a class="action-btn expire" href="/expire/{f.id}">⛔ Expire</a>
            </td>
        </tr>
        '''

    return f'''
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
        <title>Admin Dashboard 🔐</title>
        <link rel="stylesheet" href="/static/css/dashboard.css">
    </head>
    <body>
        <div class="container">
            <h1>Admin-Dashboard 🔐</h1>

            <div class="analytics-row">
                <div class="analytics-box">
                    <h3>📁 Total Files</h3>
                    <p>{total_files}</p>
                </div>
                <div class="analytics-box">
                    <h3>⬇️ Total Downloads</h3>
                    <p>{total_downloads}</p>
                </div>
                <div class="analytics-box">
                    <h3>⏰ Expired Files</h3>
                    <p>{expired_files}</p>
                </div>
            </div>

            <table>
                <tr>
                    <th>Filename</th>
                    <th>Uploaded (IST)</th>
                    <th>Expires At</th>
                    <th>Downloads</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
                {rows if rows else "<tr><td colspan='6'>No files uploaded yet.</td></tr>"}
            </table>

            <div class="footer">
                <a href="/upload">⬅ Upload</a> |
                <a href="/logout">🚪 Logout</a>
            </div>
        </div>
    </body>
    </html>
    '''
