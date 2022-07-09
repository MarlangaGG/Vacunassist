from flask import redirect, render_template

def index():
    return render_template("home.html")