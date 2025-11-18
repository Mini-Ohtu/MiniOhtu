from flask import redirect, render_template, request, jsonify, flash
from db_helper import reset_db
from repositories.todo_repository import get_todos, create_todo, set_done
from repositories.reference_repository import create_references
from config import app, test_env
from util import validate_todo


@app.route("/")
def references():
    return render_template("index.html")

@app.route("/create_book", methods=["POST"])
def save():
    new_book = {
        "author": request.form.get("author"),
        "title": request.form.get("title"),
        "year": request.form.get("year"),
        "publisher": request.form.get("publisher")
    }
    # TODO: finish saving to database
    create_references(new_book["author"], new_book["title"], new_book["year"], new_book["publisher"])

@app.route("/new_book")
def new_book():
    return render_template("new_book.html")

# testausta varten oleva reitti
if test_env:
    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({ 'message': "db reset" })
