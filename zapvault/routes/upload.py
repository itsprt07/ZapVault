from flask import Blueprint, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid
import qrcode
import pytz

from ..models.user import User
from ..models.file import File
from .. import db
from ..utils.helpers import IST

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if 'user' not in session:
        return redirect('/login')

    user = User.query.filter_by(email=session['user']).first()
    if not user:
        return redirect('/login')

    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_id = str(uuid.uuid4())
            filename = file_id + "_" + secure_filename(file.filename)
            save_path = os.path.join('uploads', filename)
            file.save(save_path)

            expiry_minutes = int(request.form.get('expiry_minutes', 5))
            expiry_time_utc = datetime.utcnow() + timedelta(minutes=expiry_minutes)
            expiry_time_ist = expiry_time_utc.replace(tzinfo=pytz.UTC).astimezone(IST)

            # ✅ Save file with user's token
            new_file = File(
                id=file_id,
                filename=filename,
                expires_at=expiry_time_utc,
                token=user.token
            )
            db.session.add(new_file)
            db.session.commit()

            download_url = url_for('download_bp.download_file', file_id=file_id, _external=True)

            qr_img = qrcode.make(download_url)
            qr_path = os.path.join('static/qrs', f'{file_id}.png')
            qr_img.save(qr_path)

            return f'''
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
    <title>Upload Success - ZapVault</title>
    <link rel="stylesheet" href="/static/css/success.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h2>✅ File Uploaded Successfully!</h2>
        <p class="info">Download link (valid for <b>{expiry_minutes}</b> minutes):</p>
        <a href="{download_url}" class="download-link">{download_url}</a><br>
        <img src="/static/qrs/{file_id}.png" alt="QR Code"><br>
        <small>📱 Scan to download</small>
        <p class="expiry">⏰ IST Expiry Time: <b>{expiry_time_ist.strftime('%Y-%m-%d %I:%M:%S %p')}</b></p>

        <div class="nav-links">
            <a href="/upload">⬆ Upload Another</a>
            <a href="/dashboard">🛠️ Dashboard</a>
        </div>
    </div>
</body>
</html>
'''

    # --- GET request: Upload Form ---
    return '''
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon">
    <title>Upload File - ZapVault</title>
    <link rel="stylesheet" href="/static/css/upload.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="upload-container">
        <h1>🚀ZapVault Uploader</h1>
        <p class="subtext">Secure, fast, and self-destructing file sharing at your fingertips.</p>

        <form method="POST" action="/upload" enctype="multipart/form-data" class="upload-form">
            <label>Browse your file:</label><br>
            <input type="file" name="file" required><br>

            <label>⏳ Set Expiry time:</label><br>
            <select name="expiry_minutes" required>
                <option value="1">1 minute</option>
                <option value="2">2 minutes</option>
                <option value="5">5 minutes</option>
                <option value="10">10 minutes</option>
                <option value="30">30 minutes</option>
                <option value="60">1 hour</option>
                <option value="1440">1 day</option>
            </select><br>

            <button type="submit">⬆ Upload</button>
        </form>

        <div class="links">
            <a href="/dashboard">🛠️ Dashboard</a> |
            <a href="/logout">🚪 Logout</a>
        </div>
    </div>
</body>
</html>
'''
