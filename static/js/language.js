document.addEventListener('DOMContentLoaded', function () {
    const languageSwitcher = document.getElementById('language-switcher');
    const currentPage = document.body.getAttribute('data-page'); // Detect the current page

    // Load the saved language from localStorage or default to 'en'
    const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
    changeLanguage(savedLanguage);
    languageSwitcher.value = savedLanguage; // Set the switcher to the saved language

    // When the language is changed
    languageSwitcher.addEventListener('change', function () {
        const selectedLanguage = this.value;
        localStorage.setItem('selectedLanguage', selectedLanguage); // Save the selected language
        changeLanguage(selectedLanguage);
    });

    function changeLanguage(language) {
        fetch(`/static/lang/${language}.json`)
            .then(response => response.json())
            .then(data => {
                // Check which page is loaded and update accordingly
                if (currentPage === "intro") {
                    document.getElementById('intro-title').textContent = data.intro.intro_title;
                    document.getElementById('intro-paragraph-1').textContent = data.intro.intro_paragraph_1;
                    document.getElementById('intro-paragraph-2').textContent = data.intro.intro_paragraph_2;
                    document.getElementById('start-btn').textContent = data.intro.start_button;
                } else if (currentPage === "survey") {
                    document.getElementById('survey-title').textContent = data.survey.survey_title;
                    document.getElementById('consent-label').textContent = data.survey.consent_label;
                    document.getElementById('yes-label').textContent = data.survey.yes_label;
                    document.getElementById('no-label').textContent = data.survey.no_label;
                    document.getElementById('patient-label').textContent = data.survey.patient_label;
                    document.getElementById('procedure-label').textContent = data.survey.procedure_label;
                    document.getElementById('gender-label').textContent = data.survey.gender_label;
                    document.getElementById('age-label').textContent = data.survey.age_label;
                    document.getElementById('religion-label').textContent = data.survey.religion_label;
                    document.getElementById('submit-button').value = data.survey.submit_button;
                } else if (currentPage === "result") {
                    document.getElementById('result-title').textContent = data.result.result_title;
                    document.getElementById('id-header').textContent = data.result.id_column;
                    document.getElementById('consent-header').textContent = data.result.consent_column;
                    document.getElementById('patient-choice-header').textContent = data.result.patient_choice_column;
                    document.getElementById('procedure-rating-header').textContent = data.result.procedure_rating_column;
                    document.getElementById('age-header').textContent = data.result.age_column;
                    document.getElementById('gender-header').textContent = data.result.gender_column;
                    document.getElementById('religion-header').textContent = data.result.religion_column;
                } else if (currentPage === "thank_you") {
                    document.getElementById('thank-you-title').textContent = data.thank_you.thank_you_title;
                    document.getElementById('thank-you-message').textContent = data.thank_you.thank_you_message;
                }
            });
    }
});
