from urllib.parse import urlencode
from flask import redirect, render_template, request, jsonify, url_for
from db_helper import reset_db
from repositories.reference_repository import get_references, create_references
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
        return redirect(f"{url_for('new')}?{query}")

@app.route("/edit_reference", methods=["POST"])
def edit_reference():
    citekey = request.form.get("citekey")
    author = request.form.get("author")
    title = request.form.get("title")
    year = request.form.get("year")
    publisher = request.form.get("publisher")

    try:
        validate_reference_title(title)
        year_value = validate_reference_year(year)
        # Updatea ei vielä ole toteutettu, eroaa uuden luomisesta, sillä ei synny uutta id:tä
        update_reference(citekey, author, title, year_value, publisher)
        return redirect(url_for("index", reference_updated="true"))
  
    except Exception as error:
        query = urlencode({"error": str(error)})
        return redirect(f"{url_for('edit_reference')}?{query}")
      
@app.route("/delete_reference/<key>", methods=["POST"])
def reference_deletion(key):
    print(key)
    print("reference will be deleted")
    # delete_reference(key)
    return redirect("/")

# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
