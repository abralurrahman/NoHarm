document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitButton = document.querySelector('input[type="submit"]');

    // Add event listener to submit button
    submitButton.addEventListener('click', function(event) {
        let isValid = true;

        // Validate text input fields (e.g., age)
        const textInputs = document.querySelectorAll('input[type="text"], input[type="number"]');
        textInputs.forEach(function(input) {
            if (input.hasAttribute('required') && input.value === "") {
                alert(`Please fill out the ${input.name.replace(/_/g, " ")} field.`);
                isValid = false;
                input.style.border = "2px solid red"; // Highlight missing input
            } else {
                input.style.border = ""; // Reset style
            }
        });

        // Validate radio button groups
        const requiredRadioGroups = ['patient_choice_1', 'patient_choice_2', 'patient_choice_3', 'rating_save_life_years', 'rating_advantage_disadvantaged', 'rating_benefit_future']; // Add all required radio groups
        requiredRadioGroups.forEach(function(group) {
            const radios = document.querySelectorAll(`input[name="${group}"]`);
            const isChecked = Array.from(radios).some(radio => radio.checked);

            if (!isChecked) {
                alert(`Please select an option for ${group.replace(/_/g, " ")}.`);
                isValid = false;
                radios[0].closest('.procedure-block').style.border = "2px solid red"; // Highlight missed group
            } else {
                radios[0].closest('.procedure-block').style.border = ""; // Reset style
            }
        });

        // Validate select fields (dropdowns)
        const selectFields = document.querySelectorAll('select[required]');
        selectFields.forEach(function(select) {
            if (select.value === "") {
                alert(`Please select an answer for ${select.name.replace(/_/g, " ")}.`);
                isValid = false;
                select.style.border = "2px solid red"; // Highlight missing select
            } else {
                select.style.border = ""; // Reset style
            }
        });

        // If any validation fails, prevent form submission
        if (!isValid) {
            event.preventDefault(); // Stop form submission
        }
    });
});
