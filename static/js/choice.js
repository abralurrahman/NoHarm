// Function to handle patient selection
function submitChoice(selectedImage) {
    const selectedInput = document.getElementById('selected-image');
    const choiceForm = document.getElementById('choice-form');

    if (selectedInput && choiceForm) {
        selectedInput.value = selectedImage;
        choiceForm.submit(); // Submit the form immediately
    } else {
        console.error("Form or input element not found for submitting choice.");
    }
}

// Function to close the popup and reload the previous page
function closePopup() {
    window.location.href = "/choice-experiment"; // Redirect to the choice experiment
}

// Event listeners for better accessibility
document.addEventListener('DOMContentLoaded', () => {
    console.log("JavaScript loaded successfully!");
});
