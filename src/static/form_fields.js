const FIELD_MAP = window.FIELD_MAP || {};

function renderFields(type) {
  // Render all fields (required + optional) for the chosen BibTeX type.
  const container = document.getElementById("fields-container");
  const typeHeading = document.getElementById("type-heading");
  if (!container || !typeHeading) return;

  const config = FIELD_MAP[type];
  const requiredFields = config[0];
  const optionalFields = config[1];

  const toLabel = (name, required) => {
    const base = name.replace(/_/g, " ");
    const pretty = base.charAt(0).toUpperCase() + base.slice(1);
    return required ? `${pretty} *` : pretty;
  };

  const existingData = (window.EXISTING_DATA && window.EXISTING_DATA.data) || {};

  const fields = [
    ...requiredFields.map((name) => ({ name, required: true })),
    ...optionalFields.map((name) => ({ name, required: false })),
  ];
  // Simple markup builder keeps HTML inline.
  container.innerHTML = fields
    .map((field) => {
      const valueAttr =
        existingData[field.name] !== undefined
          ? ` value="${String(existingData[field.name])}"`
          : "";
      return (
        `<p><label for="${field.name}">${toLabel(field.name, field.required)}</label>` +
        `<input class="form-control" type="text" id="${field.name}" name="${field.name}"${valueAttr} ${
          field.required ? "required" : ""
        }></p>`
      );
    })
    .join("");

  const prettyType = type ? type.charAt(0).toUpperCase() + type.slice(1) : "";
  typeHeading.textContent = prettyType || "Book";
}

function setupDynamicFields() {
  // Wire radio buttons to re-render fields on type change.
  const typeInputs = document.querySelectorAll('input[name="entry_type"]');
  const initial =
    (window.EXISTING_DATA && window.EXISTING_DATA.entry_type) ||
    (document.querySelector('input[name="entry_type"]:checked') || typeInputs[0] || {}).value;

  typeInputs.forEach((input) => {
    input.addEventListener("change", (event) => {
      renderFields(event.target.value);
    });
  });

  renderFields(initial || "book");
}

document.addEventListener("DOMContentLoaded", setupDynamicFields);
