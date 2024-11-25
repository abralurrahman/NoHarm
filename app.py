from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import requests
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

# Route for procedural ratings page
@app.route('/procedural-ratings')
def procedural_ratings():
    return render_template('procedural_ratings.html', language=session.get('language'))


# Route to handle procedural ratings submission and redirect to demography page
@app.route('/submit-procedural-ratings', methods=['POST'])
def submit_procedural_ratings():
    ratings = {
        'save_life_years': request.form.get('rating_save_life_years'),
        'advantage_disadvantaged': request.form.get('rating_advantage_disadvantaged'),
        'benefit_future': request.form.get('rating_benefit_future'),
        'first_come': request.form.get('rating_first_come'),
        'treatment_success': request.form.get('rating_treatment_success'),
        'treatment_effort': request.form.get('rating_treatment_effort'),
        'medication_effect': request.form.get('rating_medication_effect'),
        'random_selection': request.form.get('rating_random_selection'),
    }

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO procedural_ratings 
        (save_life_years, advantage_disadvantaged, benefit_future, first_come, 
         treatment_success, treatment_effort, medication_effect, random_selection) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 tuple(ratings.values()))
    conn.commit()
    conn.close()

    return redirect('/demography')


# Route for demography page
@app.route('/demography')
def demography():
    return render_template('demography.html', language=session.get('language'))


# Route to handle demography form submission and redirect to group preferences page
@app.route('/submit-demography', methods=['POST'])
def submit_demography():
    demographics = {
        'gender': request.form.get('gender'),
        'age': request.form.get('age'),
        'religion': request.form.get('religion'),
        'other_religion': request.form.get('other_religion') if request.form.get('religion') == 'other' else None,
    }

    conn = get_db_connection()
    conn.execute('INSERT INTO demography (gender, age, religion, other_religion) VALUES (?, ?, ?, ?)',
                 tuple(demographics.values()))
    conn.commit()
    conn.close()

    return redirect('/group-preferences')


# Route for group-related preferences page
@app.route('/group-preferences')
def group_preferences():
    return render_template('group_preferences.html', language=session.get('language'))


# Route to handle group preferences submission and then thank the user
@app.route('/submit-group-preferences', methods=['POST'])
def submit_group_preferences():
    preferences = {
        'general_health': request.form.get('general_health'),
        'illness': request.form.get('illness'),
        'children': request.form.get('children'),
    }

    conn = get_db_connection()
    conn.execute('INSERT INTO group_preferences (general_health, illness, children) VALUES (?, ?, ?)',
                 tuple(preferences.values()))
    conn.commit()
    conn.close()

    return redirect('/thank-you')


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
