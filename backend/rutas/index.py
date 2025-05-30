from flask import Blueprint, render_template, session, redirect, url_for

index_bp = Blueprint("index", __name__)

@index_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@index_bp.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index.index"))
