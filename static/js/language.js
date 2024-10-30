document.addEventListener('DOMContentLoaded', function () {
    const languageSwitcher = document.getElementById('language-switcher');
    const currentPage = document.body.getAttribute('data-page'); // Detect the current page

    // Detect user language or load saved language from localStorage
    const defaultLanguage = navigator.language.slice(0, 2); // E.g., 'en', 'fr'
    const savedLanguage = localStorage.getItem('selectedLanguage') || defaultLanguage || 'en';

    // Set and apply selected language on page load
    changeLanguage(savedLanguage);
    languageSwitcher.value = savedLanguage;

    // Change language event listener
    languageSwitcher.addEventListener('change', function () {
        const selectedLanguage = this.value;
        localStorage.setItem('selectedLanguage', selectedLanguage); // Save the selected language
        changeLanguage(selectedLanguage);
    });

    // Function to dynamically change language
    function changeLanguage(language) {
        fetch(`/static/lang/${language}.json`)
            .then(response => response.json())
            .then(data => {
                if (currentPage === "intro") {
                    document.getElementById('intro-title').textContent = data.intro.intro_title;
                    document.getElementById('intro-paragraph-1').textContent = data.intro.intro_paragraph_1;
                    document.getElementById('intro-paragraph-2').textContent = data.intro.intro_paragraph_2;
                    document.getElementById('intro-paragraph-3').textContent = data.intro.intro_paragraph_3;
                    document.getElementById('consent-title').textContent = data.intro.consent_title;
                    document.getElementById('consent-message').textContent = data.intro.consent_message;
                    document.getElementById('yes-label-span').textContent = data.intro.yes_label;
                    document.getElementById('no-label-span').textContent = data.intro.no_label;
                    document.getElementById('start-btn').textContent = data.intro.start_button;
                } else if (currentPage === "choice_experiment") {
                    document.getElementById('survey-title').textContent = data.choice_experiment.survey_title;
                    document.getElementById('patient-question').textContent = data.choice_experiment.patient_question;
                    document.getElementById('decision-pair-1').textContent = data.choice_experiment.decision_pair_1;
                    document.getElementById('decision-pair-2').textContent = data.choice_experiment.decision_pair_2;
                    document.getElementById('decision-pair-3').textContent = data.choice_experiment.decision_pair_3;
                    document.getElementById('change-decision').textContent = data.choice_experiment.change_decision;
                    document.getElementById('submit-button').textContent = data.choice_experiment.submit_button;
                    document.getElementById('patient-1-overweight-label').textContent = data.choice_experiment.patient_1_overweight;
                    document.getElementById('patient-2-disability-label').textContent = data.choice_experiment.patient_2_disability;
                    document.getElementById('patient-1-child-label').textContent = data.choice_experiment.patient_1_child;
                    document.getElementById('patient-2-elderly-couple-label').textContent = data.choice_experiment.patient_2_elderly_couple;
                    document.getElementById('patient-1-young-adult-label').textContent = data.choice_experiment.patient_1_young_adult;
                    document.getElementById('patient-2-senior-ill-label').textContent = data.choice_experiment.patient_2_senior_ill;
                } else if (currentPage === "demography") {
                    document.getElementById('demography-title').textContent = data.demography.demography_title;
                    document.getElementById('gender-question').textContent = data.demography.gender_question;
                    document.getElementById('female-text').textContent = data.demography.female_label;
                    document.getElementById('male-text').textContent = data.demography.male_label;
                    document.getElementById('diverse-text').textContent = data.demography.diverse_label;
                    document.getElementById('prefer-not-to-disclose-text').textContent = data.demography.prefer_not_to_disclose_label;
                    document.getElementById('age-question').textContent = data.demography.age_question;
                    document.getElementById('religion-question').textContent = data.demography.religion_question;
                    document.getElementById('no-religion-text').textContent = data.demography.no_religion;
                    document.getElementById('christian-text').textContent = data.demography.christian_label;
                    document.getElementById('islam-text').textContent = data.demography.islam_label;
                    document.getElementById('hinduism-text').textContent = data.demography.hinduism_label;
                    document.getElementById('buddhism-text').textContent = data.demography.buddhism_label;
                    document.getElementById('other-text').textContent = data.demography.other_label;
                    document.getElementById('submit-button').textContent = data.demography.submit_button;
                    // Add a slight delay for the placeholder translation to ensure it applies
                setTimeout(() => {
                    document.getElementById('age-placeholder').placeholder = data.demography.age_placeholder;
                }, 100);
                } else if (currentPage === "group_preferences") {
                    document.getElementById('group-preferences-title').textContent = data.group_preferences.group_preferences_title;
                    document.getElementById('general-health-question').textContent = data.group_preferences.general_health_question;
                    document.getElementById('select-answer').textContent = data.group_preferences.select_answer;
                    document.getElementById('very-poor').textContent = data.group_preferences.very_poor;
                    document.getElementById('poor').textContent = data.group_preferences.poor;
                    document.getElementById('fair').textContent = data.group_preferences.fair;
                    document.getElementById('good').textContent = data.group_preferences.good;
                    document.getElementById('very-good').textContent = data.group_preferences.very_good;
                    document.getElementById('excellent').textContent = data.group_preferences.excellent;
                    document.getElementById('illness-question').textContent = data.group_preferences.illness_question;
                    document.getElementById('illness-yes-label').textContent = data.group_preferences.illness_yes;
                    document.getElementById('illness-no-label').textContent = data.group_preferences.illness_no;
                    document.getElementById('children-question').textContent = data.group_preferences.children_question;
                    document.getElementById('children-yes-label').textContent = data.group_preferences.children_yes;
                    document.getElementById('children-no-label').textContent = data.group_preferences.children_no;
                    document.getElementById('submit-button').textContent = data.group_preferences.submit_button;
                } else if (currentPage === "procedural_ratings") {
                    document.getElementById('rating-title').textContent = data.procedural_ratings.rating_title;
                    document.getElementById('rating-intro').textContent = data.procedural_ratings.rating_intro;
                    document.getElementById('scale-indicator').textContent = data.procedural_ratings.scale_indicator;
                    document.getElementById('submit-button').textContent = data.procedural_ratings.submit_button;
                    document.getElementById('rating-save-life-years').textContent = data.procedural_ratings.rating_save_life_years;
                    document.getElementById('rating-advantage-disadvantaged').textContent = data.procedural_ratings.rating_advantage_disadvantaged;
                    document.getElementById('rating-benefit-future').textContent = data.procedural_ratings.rating_benefit_future;
                    document.getElementById('rating-first-come').textContent = data.procedural_ratings.rating_first_come;
                    document.getElementById('rating-treatment-success').textContent = data.procedural_ratings.rating_treatment_success;
                    document.getElementById('rating-treatment-effort').textContent = data.procedural_ratings.rating_treatment_effort;
                    document.getElementById('rating-medication-effect').textContent = data.procedural_ratings.rating_medication_effect;
                    document.getElementById('rating-random-selection').textContent = data.procedural_ratings.rating_random_selection;
                    // Update scale options dynamically for all select elements in this section
                    document.querySelectorAll('.procedure-block select').forEach(select => {
                        select.options[0].textContent = data.procedural_ratings.select_answer;
                        select.options[1].textContent = `${data.procedural_ratings.numbers[1]} (${data.procedural_ratings.not_fair})`;
                        select.options[2].textContent = data.procedural_ratings.numbers[2];
                        select.options[3].textContent = data.procedural_ratings.numbers[3];
                        select.options[4].textContent = data.procedural_ratings.numbers[4];
                        select.options[5].textContent = data.procedural_ratings.numbers[5];
                        select.options[6].textContent = `${data.procedural_ratings.numbers[6]} (${data.procedural_ratings.very_fair})`;
                    });
                } else if (currentPage === "thank_you") {
                    document.getElementById('thank-you-title').textContent = data.thank_you.thank_you_title;
                    document.getElementById('thank-you-message').textContent = data.thank_you.thank_you_message;
                } else if (currentPage === "no_consent") {
                    document.getElementById('no-consent-title').textContent = data.no_consent.no_consent_title;
                    document.getElementById('no-consent-message').textContent = data.no_consent.no_consent_message;
                }
            })
            .catch(error => console.error('Error loading language file:', error));
    }
});
