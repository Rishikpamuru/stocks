from flask import Flask,request, render_template

app = Flask(__name__)


{

}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cal", methods=["GET", "POST"])
def cal():
    ans = 0
    x = request.form.get("x")
    y = request.form.get("y")

    if x is not None and y is not None:
        ans = int(x) + int(y)


    return render_template("cal.html", ans=ans)