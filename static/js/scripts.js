
document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.querySelector('input[type="submit"]');
    const ageInput = document.querySelector('input[name="age"]');

    // Example: Disable submit if age is not filled
    submitButton.addEventListener('click', function(event) {
        if (ageInput.value === "") {
            alert("Please enter your age.");
            event.preventDefault(); // Stop form submission
        }
    });
});
