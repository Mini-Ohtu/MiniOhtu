from urllib.parse import urlencode
from flask import redirect, render_template, request, jsonify, url_for
from db_helper import reset_db
from repositories.reference_repository import (
    delete_reference,
    create_references,
    update_reference,
    get_reference_by_key,
    get_filtered_references,
    get_all_tags,
    get_tags_by_reference,
    add_tag,
    link_tag_to_reference,
    get_reference_id
)
from config import app, test_env
from util import (
    validate_reference_title,
    validate_reference_year,
    UserInputError,
)
from bibtex_fields import BIBTEX_FIELDS


def _require_field(value, label):
    text_value = (value or "").strip()
    if not text_value:
        raise UserInputError(f"{label} is required")
    return text_value


def _read_field(name, required):
    label = name
    raw_value = request.form.get(name, "")

    if name == "year":
        return validate_reference_year(raw_value, required)
    if name == "title":
        return validate_reference_title(raw_value)
    if required:
        return _require_field(raw_value, label)
    return raw_value


@app.route("/")
def index():
    references: list = get_filtered_references(request.args)
    return render_template("index.html", references=references)


@app.route("/new_reference")
def new():
    created = request.args.get("created") == "true"
    error_message = request.args.get("error")
    return render_template(
        "new_book.html",
        reference_created=created,
        error_message=error_message,
        field_map=BIBTEX_FIELDS,
    )


@app.route("/create_references", methods=["POST"])
def reference_creation():
    entry_type = (request.form.get("entry_type") or "book").strip().lower()
    citekey = request.form.get("citekey")
    type_config = BIBTEX_FIELDS.get(entry_type)

    try:
        citekey = _require_field(citekey, "CiteKey")
        if not type_config:
            raise UserInputError("Unsupported reference type")

        data = {}
        required_fields, optional_fields = type_config

        for field_name in required_fields:
            value = _read_field(field_name, True)
            if value is not None:
                data[field_name] = value

        for field_name in optional_fields:
            value = _read_field(field_name, False)
            if value is not None:
                data[field_name] = value

        create_references(citekey, entry_type, data)
        return redirect(url_for("new", created="true"))

    # pylint: disable=W0703
    except Exception as error:
        query = urlencode({"error": str(error)})
        return redirect(f"{url_for('new')}?{query}")


@app.route("/edit_reference/<key>", methods=["GET", "POST"])
def edit_reference(key):
    viite = get_reference_by_key(key)
    if viite is None:
        return "Reference not found", 404 
    if request.method == "GET":
        #huom. lisätty tag-metodeja
        tags=get_all_tags()
        ref_id=get_reference_id(key)
        reftags = get_tags_by_reference(ref_id) 
        return render_template(
            "edit_reference.html",
            viite=viite,
            field_map=BIBTEX_FIELDS,
            tags=tags,
            reftags=reftags,
        )
    citekey = key
    error_message = None
    entry_type = viite.entry_type
    type_config = BIBTEX_FIELDS.get(entry_type)

    try:
        data = {}
        required_fields, optional_fields = type_config if type_config else ([], [])

        for field_name in required_fields:
            value = _read_field(field_name, True)
            if value is not None:
                data[field_name] = value

        for field_name in optional_fields:
            value = _read_field(field_name, False)
            if value is not None:
                data[field_name] = value

        update_reference(citekey, data)

        viite = get_reference_by_key(key)
        success_message = "Update successful"
        return render_template(
            "edit_reference.html",
            viite=viite,
            success_message=success_message,
            field_map=BIBTEX_FIELDS,
        )

    # pylint: disable=W0718
    except Exception as error:
        error_message = str(error)
        viite = get_reference_by_key(key)
        return render_template(
            "edit_reference.html",
            viite=viite,
            error_message=error_message,
            field_map=BIBTEX_FIELDS,
        )


@app.route("/delete_reference/<key>", methods=["POST"])
def reference_deletion(key):
    delete_reference(key)
    return redirect("/")



#tägin lisäys 
# huom. tägin lisäysmahdollisuus nyt vain muokkauksessa 
# pitäisikö olla myös uuden viitteen lisäyksessä?

@app.route("/add_tag/<key>", methods=["GET", "POST"]) 
def adding_tag(key):
    viite = get_reference_by_key(key)
    if request.method == "GET":
        return render_template("new_tag.html", viite=viite)
    if request.method == "POST":
        tag_name = request.form["tag_name"]
        #olisiko parempi laittaa pudotusvalikkoon mahdollisuus kirjoittaa uusi tägi? 
        # nyt on siis templates/new_tag.html
        #if tag_name == "other":
        #    tag_name = request.form["new_tag"]       
        tag_id=add_tag(tag_name)
        reference_id=get_reference_id(key)
        #todo: if not tag_name or not tag_id or not reference_id: #tee jotain 
        try:
            #todo: tagin validointi, virheiden käsittely
            #validate_tag(tag_name)
            link_tag_to_reference(tag_id, reference_id)
            return redirect("/")
        except Exception as error:
            #tee jotain
            return  redirect("/")




# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
