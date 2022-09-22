let remove_btn_forms = document.querySelectorAll(".remove-form");
const confirmation_field = document.getElementById("confirmation-field");
const cancel_confirmation = document.getElementById("cancel-confirmation");
let confirm_recipe_removal = document.getElementById("confirm-removal");
let confirmation_recipe_name = document.querySelector(".confirmation-recipe");

for (let i = 0; i < remove_btn_forms.length; i++){
    remove_btn_forms[i].addEventListener("submit", (e)=>{
        // these form are not intended for submission, they are just to give javascript some data,
        // so i will be preventing the default submission
        e.preventDefault()
        // getting the name and id of the current recipe highlighted to be removed, then changing the confirm removal button hidden element value to the current highlited recipe_id   
        let recipe_name = remove_btn_forms[i].elements['recipe_name'].value
        let recipe_id = remove_btn_forms[i].elements['recipe_id'].value

        confirmation_recipe_name.textContent =`Are You Sure You Want To Remove "${recipe_name}" From Your Recipe Book`
        confirm_recipe_removal.elements['recipe_id'].value = recipe_id
        console.log(confirm_recipe_removal.elements['recipe_id'].value)
        confirmation_field.style.top = "0"
    })
}

cancel_confirmation.addEventListener("submit",(e)=>{
    e.preventDefault()
    confirm_recipe_removal.elements['recipe_id'].value = ""
    confirmation_field.style.top = "-100%"
})