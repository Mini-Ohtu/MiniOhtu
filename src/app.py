from urllib.parse import urlencode
from flask import redirect, render_template, request, jsonify, url_for
from db_helper import reset_db, setup_db
from repositories.reference_repository import (
    delete_reference,
    create_references,
    update_reference,
    get_reference_by_key,
    get_filtered_references,
    get_all_tags,
    get_reference_id,
    get_tags_by_reference,
    get_tags_not_in_reference,
    get_tag_by_id,
    create_tag,
    add_tag_to_reference
)
from config import app, test_env
from doi_service import fetch_reference_from_doi, DoiServiceError
from util import (
    validate_reference_title,
    validate_reference_year,
    UserInputError,
    validate_tag
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
    tags = get_all_tags()
    return render_template("index.html", references=references, tags=tags)


def _fetch_doi_prefill(doi_param):
    """Fetch DOI data for prefill; return (existing_data, citekey, error)."""
    if not doi_param:
        return None, None, None
    try:
        parsed = fetch_reference_from_doi(doi_param)
        existing_data = {
            "entry_type": parsed.get("entry_type"),
            "data": parsed.get("data") or {},
        }
        citekey_prefill = parsed.get("citekey")
        return existing_data, citekey_prefill, None
    except (UserInputError, DoiServiceError) as err:
        return None, None, str(err)


@app.route("/new_reference")
def new():
    created = request.args.get("created") == "true"
    error_message = request.args.get("error")
    existing_data, citekey_prefill, doi_error = _fetch_doi_prefill(
        request.args.get("doi")
    )
    if doi_error:
        error_message = doi_error

    return render_template(
        "new_book.html",
        reference_created=created,
        error_message=error_message,
        field_map=BIBTEX_FIELDS,
        existing_data=existing_data,
        citekey_prefill=citekey_prefill,
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
    if request.method == "GET":
        viite = get_reference_by_key(key)
        if viite is None:
            return "Reference not found", 404
        return render_template(
            "edit_reference.html",
            viite=viite,
            field_map=BIBTEX_FIELDS,
        )
    citekey = key

    error_message = None
    viite = get_reference_by_key(key)
    if viite is None:
        return "Reference not found", 404
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

@app.route("/add_tag/<key>", methods=["GET", "POST"])
def adding_tag(key):
    ref = get_reference_by_key(key)
    reference_id = get_reference_id(key)
    if request.method == "GET":
        ref_tags = get_tags_by_reference(reference_id)
        tags_left = get_tags_not_in_reference(reference_id)
        return render_template("add_tag.html", ref=ref, ref_tags=ref_tags, tags_left=tags_left)
    if request.method == "POST":
        tag_name = request.form["tag_name"]
        tag_id=create_tag(tag_name)
        add_tag_to_reference(tag_id, reference_id)
        ref_tags = get_tags_by_reference(reference_id)
        tags_left = get_tags_not_in_reference(reference_id)
        return render_template("add_tag.html", ref=ref, ref_tags=ref_tags, tags_left=tags_left)
    return  redirect("/")


@app.route("/new_tag", methods=["GET", "POST"])
def add_tag_only():
    tags = get_all_tags()
    if request.method == "GET":
        return render_template("new_tag.html", tags=tags)
    if request.method == "POST":
        tag_name = request.form["tag_name"]
        try:
            validate_tag(tag_name)
            create_tag(tag_name)
            return redirect(url_for("add_tag_only"))
        # pylint: disable=W0703
        except Exception as error:
            query = urlencode({"error": str(error)})
            return redirect(f"{url_for('add_tag_only')}?{query}")
    return  redirect("/")

@app.route("/show_tag_references/<tag_id>", methods=["GET", "POST"])
def show_tag_references(tag_id):
    tag = get_tag_by_id(tag_id)
    references: list = get_filtered_references(request.args, tag_id)
    return render_template("tags_references.html", references=references, tag=tag)


# testausta varten oleva reitti
if test_env:

    @app.route("/reset_db")
    def reset_database():
        reset_db()
        return jsonify({"message": "db reset"})
