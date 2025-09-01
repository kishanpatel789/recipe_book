const totalStepFormsInput = document.querySelector("#id_step-TOTAL_FORMS");
const minNumStepForms = parseInt(document.querySelector("#id_step-MIN_NUM_FORMS").value)
const maxNumStepForms = parseInt(document.querySelector("#id_step-MAX_NUM_FORMS").value)
const stepList = document.querySelector("#step-list");
const stepFormTemplate = document.querySelector("#step-template");
const addStepButton = document.querySelector("#add-step");
const removeStepButton = document.querySelector("#remove-step");

function addStep() {
  const formIndex = parseInt(totalStepFormsInput.value);
  if (formIndex < maxNumStepForms) {
    const newForm = stepFormTemplate.cloneNode(true);
    newForm.removeAttribute("id")
    newForm.style.display = "";  // make visible
    newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formIndex);
    newForm.querySelectorAll(".add-ingredient, .remove-ingredient")
      .forEach(btn => btn.setAttribute("data-step-index", formIndex));

    stepList.appendChild(newForm);
    totalStepFormsInput.value = formIndex + 1;
  }
}

function removeStep() {
  const formIndex = parseInt(totalStepFormsInput.value);
  if (formIndex > minNumStepForms) {
    stepList.lastElementChild.remove();
    totalStepFormsInput.value = formIndex - 1;
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

// delegate add/remove ingredient action
stepList.addEventListener("click", e => {
  if (e.target.matches(".add-ingredient")) {
    e.preventDefault();
    const stepIndex = e.target.getAttribute("data-step-index");
    console.log(`Add ingredient to step ${stepIndex}`);
    // TODO: implement add ingredient
  }

  if (e.target.matches(".remove-ingredient")) {
    e.preventDefault();
    const stepIndex = e.target.getAttribute("data-step-index");
    console.log(`Remove ingredient from step ${stepIndex}`);
    // TODO: implement remove ingredient
  }
});
