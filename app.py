from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'secret_key'  # Secret key for session management


# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Middleware to ensure the language is set for each page
@app.before_request
def set_language():
    if 'language' not in session:
        session['language'] = 'en'  # Default language is English


# Function to get random images for choice experiments
def get_random_images(total_images, selected_images):
    available_images = [i for i in range(1, total_images + 1) if i not in selected_images]
    return random.sample(available_images, 2)


# Home route to display the intro page
@app.route('/')
def intro():
    return render_template('intro.html', language=session.get('language'))


# Route to change language
@app.route('/change-language', methods=['POST'])
def change_language():
    language = request.form.get('language')
    session['language'] = language
    return redirect(request.referrer)  # Redirect back to the page the user was on


# Route to handle consent and redirect to choice experiment page or no consent page
@app.route('/submit', methods=['POST'])
def submit():
    consent = request.form.get('consent')
    if consent == 'yes':
        session['selected_images'] = []  # Initialize session to track shown images
        session['current_page'] = 1  # Start with the first page
        return redirect('/choice-experiment')
    else:
        return redirect('/no-consent')

# List of images with descriptions
IMAGES = [
    {"filename": "child_simple.jpg", "description": "Child"},
    {"filename": "Disability.jpg", "description": "Person with Disability"},
    {"filename": "old_male_female_simpler.jpg", "description": "Elderly Couple"},
    {"filename": "Overweight_simpler.jpg", "description": "Overweight Person"},
    {"filename": "test_0_0_1_1_0.jpg", "description": "Test Image 1"},
    {"filename": "test_0_0_2_3_1.jpg", "description": "Test Image 2"},
    {"filename": "test_0_2_3_3_2.jpg", "description": "Test Image 3"},
    {"filename": "test_1_0_3_2_0.jpg", "description": "Test Image 4"},
    {"filename": "test_1_3_2_2_1.jpg", "description": "Test Image 5"}
]


@app.route('/choice-experiment', methods=['GET', 'POST'])
def choice_experiment():
    if request.method == 'POST':
        # Store the selected image in the session
        selected_image = request.form.get('selected_image')
        if 'selected_images' not in session:
            session['selected_images'] = []
        session['selected_images'].append(selected_image)

        # Redirect to the ratings page after three decisions
        if len(session['selected_images']) >= 3:
            return redirect('/procedural-ratings')

        # Increment the page counter
        session['current_page'] += 1

    # Determine the current decision pair number (1, 2, or 3)
    page = session.get('current_page', 1)

    # Select two random images that haven't been used yet
    used_images = set(session.get('selected_images', []))
    available_images = [img for img in IMAGES if img["filename"] not in used_images]

    # Ensure exactly two images are available for the pair
    if len(available_images) >= 2:
        images = random.sample(available_images, 2)
    else:
        return redirect('/procedural-ratings')  # Fallback if fewer than two images are available

    return render_template('choice_experiment.html', images=images, page=page)

@app.route('/procedural-ratings', methods=['GET', 'POST'])
def procedural_ratings():
    # Define procedural rating questions
    questions = [
        {
            "id": "save_life_years",
            "label": "Save the most life years: prioritize those who have the most life years left after overcoming the disease (e.g., treat younger patients first)."
        },
        {
            "id": "advantage_disadvantaged",
            "label": "Provide advantage to the disadvantaged: prioritize those who are worse off than others (e.g., treat the sickest patients first)."
        },
        {
            "id": "benefit_future",
            "label": "Benefit to others in the future: prioritize those likely to make contributions to others (e.g., treat patients who have children or plan to)."
        },
        {
            "id": "first_come",
            "label": "First-come, first-served: prioritize those who were first in line (e.g., treat patients who arrived first at the hospital)."
        },
        {
            "id": "treatment_success",
            "label": "Maximize treatment success: prioritize those with the highest probability of survival after treatment (e.g., treat patients with the highest chance of recovery)."
        },
        {
            "id": "treatment_effort",
            "label": "Minimize treatment effort: prioritize those who will be cured with minimum effort (e.g., treat patients who need the least medication)."
        },
        {
            "id": "medication_effect",
            "label": "Maximize the medication effect: prioritize those where improvement per medication is highest (e.g., treat patients who benefit most from the medication)."
        },
        {
            "id": "random_selection",
            "label": "Random selection: allocate treatment by lottery (e.g., no individual characteristics considered)."
        },
    ]

    if request.method == 'POST':
        # Save the current question's response
        question_id = request.form.get('question_id')
        rating = request.form.get('rating')

        if 'ratings' not in session:
            session['ratings'] = {}

        session['ratings'][question_id] = rating

        # Determine the next question index
        current_index = int(request.form.get('current_index', 0))
        next_index = current_index + 1

        # If all questions are answered, save to DB and redirect
        if next_index >= len(questions):
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO procedural_ratings 
                (save_life_years, advantage_disadvantaged, benefit_future, first_come, 
                 treatment_success, treatment_effort, medication_effect, random_selection) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                [session['ratings'].get(q['id']) for q in questions])
            conn.commit()
            conn.close()

            session.pop('ratings', None)  # Clear the session
            return redirect('/demography')

        # Redirect to the next question
        return redirect(f'/procedural-ratings?index={next_index}')

    # Render the current question
    current_index = int(request.args.get('index', 0))
    question = questions[current_index]
    return render_template('procedural_ratings.html', question=question, index=current_index)


@app.route('/demography', methods=['GET', 'POST'])
def demography():
    # Define demographic questions
    questions = [
        {
            "id": "gender",
            "label": "What describes you best?",
            "type": "radio",
            "options": [
                {"value": "female", "label": "Female"},
                {"value": "male", "label": "Male"},
                {"value": "diverse", "label": "Diverse"},
                {"value": "prefer_not_to_disclose", "label": "Prefer not to disclose"}
            ]
        },
        {
            "id": "age",
            "label": "How old are you?",
            "type": "number",
            "placeholder": "Age (in years)"
        },
        {
            "id": "religion",
            "label": "Do you identify yourself with any of the following religions?",
            "type": "radio",
            "options": [
                {"value": "none", "label": "No, I do not"},
                {"value": "christian", "label": "Christian"},
                {"value": "islam", "label": "Islam"},
                {"value": "hinduism", "label": "Hinduism"},
                {"value": "buddhism", "label": "Buddhism"},
                {"value": "other", "label": "Other"}
            ]
        },
    ]

    if request.method == 'POST':
        # Save the current question's answer
        question_id = request.form.get('question_id')
        answer = request.form.get('answer')

        if 'demography_answers' not in session:
            session['demography_answers'] = {}

        session['demography_answers'][question_id] = answer

        # Determine the next question index
        current_index = int(request.form.get('current_index', 0))
        next_index = current_index + 1

        if next_index >= len(questions):
            # Save all answers to the database when all questions are answered
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO demography (gender, age, religion, other_religion)
                VALUES (?, ?, ?, ?)''',
                (
                    session['demography_answers'].get('gender'),
                    session['demography_answers'].get('age'),
                    session['demography_answers'].get('religion'),
                    session['demography_answers'].get('other_religion')
                )
            )
            conn.commit()
            conn.close()

            session.pop('demography_answers', None)  # Clear session answers
            return redirect('/group-preferences')

        # Redirect to the next question
        return redirect(f'/demography?index={next_index}')

    # Get the current question index
    current_index = int(request.args.get('index', 0))
    question = questions[current_index]

    return render_template('demography.html', question=question, index=current_index)

# Route for group-related preferences page
@app.route('/group-preferences', methods=['GET', 'POST'])
def group_preferences():
    questions = [
        {
            "id": "general_health",
            "label": "How is your health in general?",
            "type": "select",
            "options": ["Very Poor", "Poor", "Fair", "Good", "Very Good", "Excellent"]
        },
        {
            "id": "illness",
            "label": "Have you been severely ill in the last year?",
            "type": "radio",
            "options": [{"value": "yes", "label": "Yes"}, {"value": "no", "label": "No"}]
        },
        {
            "id": "children",
            "label": "Do you have children or are you planning to have children?",
            "type": "radio",
            "options": [{"value": "yes", "label": "Yes"}, {"value": "no", "label": "No"}]
        }
    ]

    if request.method == 'POST':
        # Save the current question's answer
        question_id = request.form.get('question_id')
        answer = request.form.get('answer')

        if 'preferences' not in session:
            session['preferences'] = {}

        session['preferences'][question_id] = answer

        # Determine the next question index
        current_index = int(request.form.get('current_index', 0))
        next_index = current_index + 1

        if next_index >= len(questions):
            # Save all answers to the database when all questions are answered
            conn = get_db_connection()
            conn.execute(
                '''
                INSERT INTO group_preferences (general_health, illness, children)
                VALUES (?, ?, ?)
                ''',
                [session['preferences'].get(q['id']) for q in questions]
            )
            conn.commit()
            conn.close()
            session.pop('preferences', None)  # Clear session preferences
            return redirect('/thank-you')
        else:
            return redirect(f'/group-preferences?index={next_index}')

    # Get the current question index
    current_index = int(request.args.get('index', 0))
    question = questions[current_index]

    return render_template('group_preferences.html', question=question, index=current_index)


# Route to thank users after survey submission
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html', language=session.get('language'))


# Route for no consent page
@app.route('/no-consent')
def no_consent():
    return render_template('no_consent.html', language=session.get('language'))


# Route for admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'admin':
            session['admin'] = True
            return redirect('/results')
        else:
            return "Incorrect password. Try again."
    return render_template('admin_login.html', language=session.get('language'))


# Route to view survey results (admin only)
@app.route('/results')
def results():
    if 'admin' in session:
        conn = get_db_connection()
        choices = conn.execute('SELECT * FROM choices').fetchall()
        procedural_ratings = conn.execute('SELECT * FROM procedural_ratings').fetchall()
        demography = conn.execute('SELECT * FROM demography').fetchall()
        group_preferences = conn.execute('SELECT * FROM group_preferences').fetchall()
        conn.close()

        return render_template('results.html',
                               choices=choices,
                               procedural_ratings=procedural_ratings,
                               demography=demography,
                               group_preferences=group_preferences,
                               language=session.get('language'))
    else:
        return redirect('/admin')


# Route to logout admin
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)
