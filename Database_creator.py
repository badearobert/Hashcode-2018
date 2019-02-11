from application import app
from Database import db

with app.app_context():
    db.init_app(app)
    db.create_all()
exit()