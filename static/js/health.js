// Health Gradient Selection
document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".health-circle-btn");
    const hiddenInput = document.getElementById("healthValue");
    const form = document.querySelector("form");

    if (buttons.length > 0) {
        buttons.forEach(button => {
            button.addEventListener("click", function () {
                // Remove existing selections
                buttons.forEach(btn => btn.classList.remove("selected"));

                // Add selection to clicked button
                this.classList.add("selected");

                // Update hidden input value
                const value = this.dataset.value;
                hiddenInput.value = value;

                // ✅ Auto-submit the form after selection
                if (value) {
                    form.submit();
                }
            });
        });
    }
});
