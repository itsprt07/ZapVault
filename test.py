# test.py

from zapvault import create_app, db
from zapvault.models.user import User

# Create app and app context
app = create_app()

with app.app_context():
    users = User.query.all()
    for user in users:
        print("Email:", user.email)
        print("Hashed Password:", user.password)
        print("Token:", user.token)
        print("---")
