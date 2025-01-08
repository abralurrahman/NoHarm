from flask import Flask, render_template, request, redirect, session, url_for
from flask import Response
import csv
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

# Update the filename paths to use the resized directory
for image in IMAGES:
    image["filename"] = f"resized_images/{image['filename']}"


@app.route('/choice-experiment', methods=['GET', 'POST'])
def choice_experiment():
    if request.method == 'POST':
        # Store the selected image in the session
        selected_image = request.form.get('selected_image')
        if 'selected_images' not in session:
            session['selected_images'] = []
        session['selected_images'].append(selected_image)

        # Redirect to the reconsideration page after three decisions
        if len(session['selected_images']) >= 3:
            return redirect('/reconsider-decision')

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
        return redirect('/reconsider-decision')  # Fallback if fewer than two images are available

    return render_template('choice_experiment.html', images=images, page=page)
@app.route('/reconsider-decision', methods=['GET', 'POST'])
def reconsider_decision():
    if request.method == 'POST':
        # Retrieve the reconsideration choice from the form
        reconsider_choice = request.form.get('reconsider')

        # Save the user's decisions into the database
        conn = get_db_connection()
        conn.execute(
            '''
            INSERT INTO user_responses (choice1, choice2, choice3, reconsider_choice)
            VALUES (?, ?, ?, ?)
            ''',
            (
                session['selected_images'][0] if len(session['selected_images']) > 0 else None,
                session['selected_images'][1] if len(session['selected_images']) > 1 else None,
                session['selected_images'][2] if len(session['selected_images']) > 2 else None,
                reconsider_choice
            )
        )
        conn.commit()
        conn.close()

        # Redirect based on the reconsideration choice
        if reconsider_choice == 'yes':
            return redirect('/choice-experiment')  # Allow the user to change their decision
        else:
            return redirect('/procedural-ratings')  # Proceed to the next step

    # Retrieve a random selected image for reconsideration
    if 'selected_images' in session and session['selected_images']:
        reconsider_image = random.choice(session['selected_images'])
    else:
        return redirect('/choice-experiment')  # Fallback if no images were selected

    # Render the reconsideration page
    return render_template('reconsider_decision.html', reconsider_image=reconsider_image)

@app.route('/procedural-ratings', methods=['GET', 'POST'])
def procedural_ratings():
    # List of questions with short IDs and full labels
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
        # Get the current question's ID and user's response
        question_id = request.form.get('question_id')
        rating = request.form.get('rating')

        # Initialize session for ratings if not already done
        if 'ratings' not in session:
            session['ratings'] = {}

        # Store the response using the question's ID
        session['ratings'][question_id] = rating

        # Move to the next question
        current_index = next((i for i, q in enumerate(questions) if q['id'] == question_id), -1)
        next_index = current_index + 1

        if next_index >= len(questions):
            # Save all responses to the database
            conn = get_db_connection()
            conn.execute('''
                UPDATE user_responses
                SET save_life_years = ?, advantage_disadvantaged = ?, benefit_future = ?, first_come = ?,
                    treatment_success = ?, treatment_effort = ?, medication_effect = ?, random_selection = ?
                WHERE id = (SELECT MAX(id) FROM user_responses)
            ''', [
                session['ratings'].get('save_life_years'),
                session['ratings'].get('advantage_disadvantaged'),
                session['ratings'].get('benefit_future'),
                session['ratings'].get('first_come'),
                session['ratings'].get('treatment_success'),
                session['ratings'].get('treatment_effort'),
                session['ratings'].get('medication_effect'),
                session['ratings'].get('random_selection'),
            ])
            conn.commit()
            conn.close()

            # Clear the ratings session data
            session.pop('ratings', None)
            return redirect('/demography')

        # Redirect to the next question
        return redirect(f'/procedural-ratings?index={next_index}')

    # Get the current question based on the index in the query parameter
    current_index = int(request.args.get('index', 0))
    question = questions[current_index]
    return render_template('procedural_ratings.html', question=question, index=current_index)


@app.route('/demography', methods=['GET', 'POST'])
def demography():
    # List of demographic questions with short IDs and full labels
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
        # Get the current question's ID and user's response
        question_id = request.form.get('question_id')
        answer = request.form.get('answer')

        # Initialize session for demographic answers if not already done
        if 'demography_answers' not in session:
            session['demography_answers'] = {}

        # Store the response using the question's ID
        session['demography_answers'][question_id] = answer

        # Move to the next question
        current_index = next((i for i, q in enumerate(questions) if q['id'] == question_id), -1)
        next_index = current_index + 1

        if next_index >= len(questions):
            # Save all responses to the database
            conn = get_db_connection()
            conn.execute('''
                UPDATE user_responses
                SET gender = ?, age = ?, religion = ?
                WHERE id = (SELECT MAX(id) FROM user_responses)
            ''', [
                session['demography_answers'].get('gender'),
                session['demography_answers'].get('age'),
                session['demography_answers'].get('religion'),
            ])
            conn.commit()
            conn.close()

            # Clear the demographic answers session data
            session.pop('demography_answers', None)
            return redirect('/group-preferences')

        # Redirect to the next question
        return redirect(f'/demography?index={next_index}')

    # Get the current question based on the index in the query parameter
    current_index = int(request.args.get('index', 0))
    question = questions[current_index]
    return render_template('demography.html', question=question, index=current_index)


@app.route('/group-preferences', methods=['GET', 'POST'])
def group_preferences():
    # List of group preference questions with short IDs and full labels
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
        # Get the current question's ID and user's response
        question_id = request.form.get('question_id')
        answer = request.form.get('answer')

        # Initialize session for group preferences if not already done
        if 'preferences' not in session:
            session['preferences'] = {}

        # Store the response using the question's ID
        session['preferences'][question_id] = answer

        # Move to the next question
        current_index = next((i for i, q in enumerate(questions) if q['id'] == question_id), -1)
        next_index = current_index + 1

        if next_index >= len(questions):
            # Save all responses to the database
            try:
                conn = get_db_connection()
                conn.execute('''
                    UPDATE user_responses
                    SET general_health = ?, illness = ?, children = ?
                    WHERE id = (SELECT MAX(id) FROM user_responses)
                ''', [
                    session['preferences'].get('general_health'),
                    session['preferences'].get('illness'),
                    session['preferences'].get('children'),
                ])
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error saving group preferences: {e}")
                return "An error occurred while saving your responses. Please try again."

            # Clear the session preferences data
            session.pop('preferences', None)
            return redirect('/thank-you')

        # Redirect to the next question
        return redirect(f'/group-preferences?index={next_index}')

    # Get the current question based on the index in the query parameter
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


@app.route('/results')
def results():
    if 'admin' in session:
        # Connect to the database
        conn = get_db_connection()

        # Fetch all user responses
        user_responses = conn.execute('SELECT * FROM user_responses').fetchall()
        conn.close()

        # Render the results page with user responses
        return render_template('results.html', user_responses=user_responses)

    # If the user is not logged in as admin, redirect to admin login
    return redirect('/admin')

from flask import Response
import csv

@app.route('/download-csv')
def download_csv():
    if 'admin' in session:
        # Connect to the database
        conn = get_db_connection()
        user_responses = conn.execute('SELECT * FROM user_responses').fetchall()
        conn.close()

        # Prepare the CSV content
        def generate_csv():
            # Create a CSV output
            output = []
            # Write header row (column names)
            output.append(",".join([key for key in user_responses[0].keys()]))

            # Write each row
            for row in user_responses:
                output.append(",".join([str(row[key]) for key in row.keys()]))

            return "\n".join(output)

        # Generate the CSV content
        csv_content = generate_csv()

        # Create a Response object for the CSV file
        response = Response(csv_content, mimetype='text/csv')
        response.headers.set("Content-Disposition", "attachment", filename="survey_results.csv")
        return response

    return redirect('/admin')  # Redirect to admin login if not logged in



# Route to logout admin
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)
