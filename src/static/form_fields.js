const FIELD_MAP = window.FIELD_MAP || {};

function renderFields(type) {
  // Render all fields (required + optional) for the chosen BibTeX type.
  const container = document.getElementById("fields-container");
  const typeHeading = document.getElementById("type-heading");
  if (!container || !typeHeading) return;

  const config = FIELD_MAP[type];
  const requiredFields = config.required;
  const optionalFields = config.optional;

  const fields = [...requiredFields, ...optionalFields];
  // Simple markup builder keeps HTML inline.
  container.innerHTML = fields
    .map(
      (field) =>
        `<p><label for="${field.name}">${field.label || field.name}</label><br>` +
        `<input type="text" id="${field.name}" name="${field.name}" ${
          field.required ? "required" : ""
        }></p>`
    )
    .join("");

  const prettyType = type ? type.charAt(0).toUpperCase() + type.slice(1) : "";
  typeHeading.textContent = prettyType || "Book";
}

function setupDynamicFields() {
  // Wire radio buttons to re-render fields on type change.
  const typeInputs = document.querySelectorAll('input[name="entry_type"]');
  const initial =
    document.querySelector('input[name="entry_type"]:checked') ||
    typeInputs[0];

  typeInputs.forEach((input) => {
    input.addEventListener("change", (event) => {
      renderFields(event.target.value);
    });
  });

  renderFields(initial ? initial.value : "book");
}

document.addEventListener("DOMContentLoaded", setupDynamicFields);
