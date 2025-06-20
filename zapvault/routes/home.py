from flask import Blueprint, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from zapvault.models.user import User
from zapvault.utils.helpers import render_home
from zapvault import db

import random
import re

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def home():
    print("✅ Home page hit")

    form = request.args.get('form', 'login')

    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password'].strip()

        # ✅ Login
        if 'login' in request.form:
            token = request.form['token'].strip()
            user = User.query.filter_by(email=email).first()

            if user:
                print("🔍 User found:", email)
                if check_password_hash(user.password, password):
                    if user.token == token:
                        print("✅ Token matched")
                        session['user'] = email
                        return redirect('/upload')
                    else:
                        print("❌ Invalid token")
                        return render_home(message='❌ Invalid token', form='login')
                else:
                    print("❌ Incorrect password")
            else:
                print("❌ User not found:", email)

            return render_home(message='❌ Invalid login credentials', form='login')

        # ✅ Signup
        elif 'signup' in request.form:
            if not email.endswith('@gmail.com'):
                print("❌ Non-Gmail attempted:", email)
                return render_home(message='⚠️ Only Gmail addresses are allowed', form='signup')

            if User.query.filter_by(email=email).first():
                print("⚠️ Email already exists:", email)
                return render_home(message='⚠️ Email already exists', form='signup')

            if len(password) < 8:
                return render_home(message='🔒 Password must be at least 8 characters', form='signup')
            if not re.fullmatch(r'[a-z0-9]+', password):
                return render_home(message='🔐 Password must contain only lowercase letters (a-z) and digits (0–9)', form='signup')

            token = str(random.randint(100000, 999999))
            hashed_pw = generate_password_hash(password)
            new_user = User(email=email, password=hashed_pw, token=token)
            db.session.add(new_user)
            db.session.commit()
            print(f"✅ New user registered: {email} with token: {token}")

            return render_home(message=f'✅ Account created. Your token is <b>{token}</b>. Use it during login.', form='login')

    return render_home(form=form)

