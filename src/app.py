from urllib.parse import urlencode
from flask import redirect, render_template, request, jsonify, url_for
from db_helper import reset_db
from repositories.reference_repository import (
    delete_reference,
    get_references,
    create_references,
    update_reference,
    get_reference_by_key
)
from config import app, test_env
from util import validate_reference_title, validate_reference_year


@app.route("/")
def index():
    references = get_references()
    return render_template("index.html", references=references)


@app.route("/new_book")
def new():
    created = request.args.get("created") == "true"
    error_message = request.args.get("error")
    return render_template(
        "new_book.html", book_created=created, error_message=error_message
    )


@app.route("/create_references", methods=["POST"])
def reference_creation():
    citekey = request.form.get("citekey")
    author = request.form.get("author")
    title = request.form.get("title")
    year = request.form.get("year")
    publisher = request.form.get("publisher")

    try:
        validate_reference_title(title)
        year_value = validate_reference_year(year)

        create_references(citekey, author, title, year_value, publisher)
        return redirect(url_for("new", created="true"))

    # pylint: disable=W0703
    except Exception as error:
        query = urlencode({"error": str(error)})
        return redirect(f"{url_for("new")}?{query}")


@app.route("/edit_reference/<key>", methods=["GET", "POST"])
def edit_reference(key):
    if request.method == "GET":
        viite = get_reference_by_key(key)
        if viite is None:
            return "Reference not found", 404
        return render_template("edit_reference.html", viite=viite)
    citekey = key
    author = request.form.get("author")
    title = request.form.get("title")
    year = request.form.get("year")
    publisher = request.form.get("publisher")

    error_message = None

    try:
        validate_reference_title(title)
        validate_reference_year(year)

        update_reference(citekey, author, title, year, publisher)

        viite = get_reference_by_key(key)
        success_message = "Päivitys onnistui"
        return render_template("edit_reference.html", viite=viite, success_message=success_message)

    # pylint: disable=W0718
    except Exception as error:
        error_message = str(error)
        viite = get_reference_by_key(key)
        return render_template("edit_reference.html", viite=viite, error_message=error_message)


@app.route("/delete_reference/<key>", methods=["POST"])
def reference_deletion(key):
    delete_reference(key)
    return redirect("/")


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
