from main import app, db
from os import remove

try:
    remove("instance/stocks.db")
except:
    pass

with app.app_context():
    db.create_all()