from flask import Flask, request, render_template, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import base64
import random
import hashlib

USERNAME = "admin"
PASSWORD = "admin"

def md5(text):
    return hashlib.md5(text.encode("utf-8")).digest().hex()

db = SQLAlchemy()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stocks.db"



app.secret_key = base64.b64encode(random.randbytes(16)).decode("utf-8")
db.init_app(app)


class User(db.Model):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False )
    password = db.Column(db.String, nullable=False)


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    symbol = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer,default=1, nullable=False)
    user = db.Column(db.Integer , db.ForeignKey(User.id), primary_key=False)



def get_current_user():
    userid = session.get("userid")
    user = db.session.query(User).get(userid)
    return user



@app.route("/")
def index():
    user = get_current_user()
    return render_template("index.html", username=session.get("username"))

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method =="POST":
        try:
            username = request.form["username"]
            password = md5(request.form["password"])
            if username and password:
                user = User(username = username, password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                return render_template("signup.html", error="no empty strings")
        except Exception as error:
            return render_template("signup.html", error=error)
    return render_template("signup.html")

@app.route("/login",methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password =  md5(request.form.get("password"))

        username = db.session.query(User).filter_by(username=username).first()
        if username and username .password == password:
            session["userid"] = username.id
            return redirect(url_for("index"))
        else:
            flash("invalid login!!!!!!!!!!!!!!!")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect(url_for("login"))