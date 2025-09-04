const totalStepFormsInput = document.querySelector("#id_step-TOTAL_FORMS");
const minNumStepForms = parseInt(document.querySelector("#id_step-MIN_NUM_FORMS").value)
const maxNumStepForms = parseInt(document.querySelector("#id_step-MAX_NUM_FORMS").value)
const stepList = document.querySelector("#step-list");
const stepFormTemplate = document.querySelector("#step-template");
const addStepButton = document.querySelector("#add-step");
const removeStepButton = document.querySelector("#remove-step");


const totalStepIngredientFormsInput = document.querySelector("#id_stepingr-TOTAL_FORMS");
const stepIngredientFormTemplate = document.querySelector("#step-ingredient-template");

function addStep() {
  const stepIndex = parseInt(totalStepFormsInput.value);
  if (stepIndex < maxNumStepForms) {
    const newStep = stepFormTemplate.cloneNode(true);
    newStep.removeAttribute("id")
    newStep.style.display = "";  // make visible
    newStep.innerHTML = newStep.innerHTML.replace(/__prefix__/g, stepIndex);

    newStep.dataset.stepIndex = stepIndex;

    stepList.appendChild(newStep);
    totalStepFormsInput.value = stepIndex + 1;
  }
}

function removeStep() {
  const stepIndex = parseInt(totalStepFormsInput.value);
  if (stepIndex > minNumStepForms) {
    stepList.lastElementChild.remove();
    totalStepFormsInput.value = stepIndex - 1;
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

function addIngredient(stepIndex) {
  const ingredientIndex = parseInt(totalStepIngredientFormsInput.value);

  const newIngredient = stepIngredientFormTemplate.cloneNode(true);
  newIngredient.removeAttribute("id");
  newIngredient.style.display = "";
  newIngredient.innerHTML = newIngredient.innerHTML.replace(/__prefix__/g, ingredientIndex);
  newIngredient.innerHTML = newIngredient.innerHTML.replace(/__stepIndex__/g, stepIndex);

  const stepItem = stepList.querySelector(`li[data-step-index="${stepIndex}"]`);
  const ingredientList = stepItem.querySelector(".ingredient-list");
  ingredientList.appendChild(newIngredient);

  totalStepIngredientFormsInput.value = ingredientIndex + 1;
}

function removeIngredient(stepIndex) {
  const stepItem = stepList.querySelector(`li[data-step-index="${stepIndex}"]`);
  const ingredientList = stepItem.querySelector(".ingredient-list");
  if (ingredientList.lastElementChild) {
    ingredientList.lastElementChild.remove();
    totalStepIngredientFormsInput.value =
      parseInt(totalStepIngredientFormsInput.value) - 1;
  }
}

// delegate add/remove ingredient action
stepList.addEventListener("click", e => {
  const addBtn = e.target.closest(".add-ingredient");
  if (addBtn) {
    e.preventDefault();
    const stepIndex = e.target.closest("li").getAttribute("data-step-index");
    addIngredient(stepIndex);
  }

  const removeBtn = e.target.closest(".remove-ingredient");
  if (removeBtn) {
    e.preventDefault();
    const stepIndex = e.target.closest("li").getAttribute("data-step-index");
    removeIngredient(stepIndex);
  }
});
