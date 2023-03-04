from flask import Flask, render_template, redirect, session, request, json
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "#$secret23&"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///singin.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.permanenet_session_lifetime = timedelta(days=7)

with open("config.json", "r") as g:
    secure = json.load(g)["admin"]

class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(5000), nullable=False)

class Singin(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route("/")
def home():
    if "Email" not in session:
        a = "a"

    else:
        a = "b"
    return render_template("index.html", b=a)

@app.route("/services")
def service():
    if "Email" not in session:
        a = "a"

    else:
        a = "b"
    return render_template("service.html", b=a)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if "Email" not in session:
        a = "a"

    else:
        a = "b"
    if request.method == "POST":
        naam = request.form['name']
        emai = request.form['email']
        sub = request.form['subject']
        mess = request.form['message']
        con = Contact(name=naam, email=emai, subject=sub, message=mess)
        db.session.add(con)
        db.session.commit()
        return redirect("/")

    return render_template("contact.html", b=a)

@app.route("/view", methods=["GET", "POST"])
def view():
    if "Email" not in session:
        a = "a"

    else:
        a = "b"
    
    if request.method == "POST":
        admin = request.form['admin']
        passsword = request.form['pas']

        if admin == secure['username'] and passsword == secure['password']:
            session["admin"] = admin
            return render_template("view.html", values=Contact.query.all(), b=a, val=Singin.query.all())
    if "admin" in session and session["admin"] == secure["username"]:
        return render_template("view.html", values=Contact.query.all(), b=a, val=Singin.query.all())

    return render_template("sec.html")

@app.route("/b")
def ba():
    session.pop("admin")
    return redirect("/")

@app.route("/delete/<int:sno>")
def dele(sno):
    cont = Contact.query.filter_by(sno=sno).first()
    db.session.delete(cont)
    db.session.commit()
    return redirect("/view")

@app.route("/del/<int:sno>")
def de(sno):
    sg = Singin.query.filter_by(sno=sno).first()
    db.session.delete(sg)
    db.session.commit()
    return redirect("/view")

@app.route("/sign", methods=["GET", "POST"])
def sign():
    if "Email" not in session:
        a = "a"

    else:
        a = "b"

    c = "d"
    if request.method == "POST":
        Name = request.form['name']
        Email = request.form['email']
        Password = request.form['password']
        user_name = Singin.query.filter_by(name=Name).first()
        user_email = Singin.query.filter_by(email=Email).first()
        if user_name or user_email:
            print("already")
        else:
            sig = Singin(name=Name, email=Email, password=Password)
            db.session.add(sig)
            db.session.commit()
            session["Email"] = Email
            session.permanent=True
            return redirect("/")

    return render_template("singn.html", b=a, d=c)

@app.route("/Login", methods=["GET", "POST"])
def Log():
    if "Email" not in session:
        a = "a"

    else:
        a = "b"
    c = "f"
    if request.method == "POST":
        Name = request.form['name']
        Email = request.form['email']
        Password = request.form['password']
        find_name = Singin.query.filter_by(name=Name).first()
        find_email = Singin.query.filter_by(email=Email).first()
        find_passs = Singin.query.filter_by(password=Password).first()
        if find_name and find_email and find_passs:
            session["Email"] = find_email.email
            session.permanent=True

            return redirect("/")

        else:
            print("this is not exist please go and sign up")
            return redirect("/Login")
    
    return render_template("singn.html", b=a, d=c) 

@app.route("/Logout")
def out():
    session.pop("Email")
    return redirect("/")

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)