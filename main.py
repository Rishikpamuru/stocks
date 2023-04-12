from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET", "POST"])
def login():

    if request.method == "POST":

        return redirect(url_for("index"))
    
    return render_template("login.html")

