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
    return db.session.query(User).get(userid)

def current_username():
    user = get_current_user()
    return user .username if user else None




@app.route("/")
def index():
    user = get_current_user()
    return render_template("index.html", username=current_username())

@app.route("/account")
def account():

    user = get_current_user()


    stocks = db.session.query(Stock).filter_by(user=user.id).all()
    return render_template("account.html", stocks=stocks)

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        user = get_current_user()

        name = request.form["name"]
        symbol = request.form["symbol"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        if user:
            stock = Stock(name=name, symbol =symbol,
                         price=price, quantity=quantity,
                          user=user.id)
            db.session.add(stock)
            db.session.commit()
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

        user = db.session.query(User).filter_by(username=username).first()
        if user and user.password == password:
            session["userid"] = user.id
            return redirect(url_for("index"))
        else:
            flash("invalid login!!!!!!!!!!!!!!!")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    del session["userid"]
    return redirect(url_for("login"))