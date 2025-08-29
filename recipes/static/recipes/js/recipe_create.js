const totalFormsInput = document.querySelector("#id_step-TOTAL_FORMS");
const minNumForms = parseInt(document.querySelector("#id_step-MIN_NUM_FORMS").value)
const maxNumForms = parseInt(document.querySelector("#id_step-MAX_NUM_FORMS").value)
const stepList = document.querySelector("#step-list");
const emptyFormTemplate = document.querySelector("#step-template");
const addStepButton = document.querySelector("#add-step");
const removeStepButton = document.querySelector("#remove-step");

function addStep() {
  const formIndex = parseInt(totalFormsInput.value);
  if (formIndex < maxNumForms) {
    const newForm = emptyFormTemplate.cloneNode(true);
    newForm.removeAttribute("id")
    newForm.style.display = "";  // make visible
    newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formIndex);

    stepList.appendChild(newForm);
    totalFormsInput.value = formIndex + 1;
  }
}

function removeStep() {
  const formIndex = parseInt(totalFormsInput.value);
  if (formIndex > minNumForms) {
    stepList.lastElementChild.remove();
    totalFormsInput.value = formIndex - 1;
  }
}

addStepButton.addEventListener("click", (e) => {
  e.preventDefault();
  addStep();
});

removeStepButton.addEventListener("click", (e) => {
  e.preventDefault();
  removeStep();
});
