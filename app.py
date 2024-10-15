from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = 'secret_key'  # Secret key need to be added for session management

# Connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to get geolocation from IP address
def get_geolocation(ip_address):
    response = requests.get(f'http://ipinfo.io/{ip_address}/json')
    if response.status_code == 200:
        data = response.json()
        return {
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            'loc': data.get('loc')  # Latitude and Longitude
        }
    else:
        return None

# Middleware to ensure the language is set for each page
@app.before_request
def set_language():
    if 'language' not in session:
        session['language'] = 'en'  # Default language is English

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

# Route to handle form submission and redirect to choice experiment page or no consent page
@app.route('/submit', methods=['POST'])
def submit():
    consent = request.form.get('consent')
    if consent == 'yes':
        return redirect('/choice-experiment')
    else:
        return redirect('/no-consent')

# Route for the Choice & Vignettes Experiments page
@app.route('/choice-experiment')
def choice_experiment():
    return render_template('choice_experiment.html', language=session.get('language'))

# Route to handle visual choice experiment submission and redirect to procedural ratings page
@app.route('/submit-choices', methods=['POST'])
def submit_choices():
    patient_choice_1 = request.form.get('patient_choice_1')
    patient_choice_2 = request.form.get('patient_choice_2')
    patient_choice_3 = request.form.get('patient_choice_3')

    # Capture the user's IP address and geolocation
    ip_address = request.remote_addr
    geolocation = get_geolocation(ip_address)
    city = geolocation.get('city') if geolocation else None
    region = geolocation.get('region') if geolocation else None
    country = geolocation.get('country') if geolocation else None

    conn = get_db_connection()
    conn.execute('INSERT INTO choices (patient_choice_1, patient_choice_2, patient_choice_3, ip_address, city, region, country) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (patient_choice_1, patient_choice_2, patient_choice_3, ip_address, city, region, country))
    conn.commit()
    conn.close()

    return redirect('/procedural-ratings')

# Route for procedural ratings page
@app.route('/procedural-ratings')
def procedural_ratings():
    return render_template('procedural_ratings.html', language=session.get('language'))

# Route to handle procedural ratings submission and redirect to demography page
@app.route('/submit-procedural-ratings', methods=['POST'])
def submit_procedural_ratings():
    rating_save_life_years = request.form.get('rating_save_life_years')
    rating_advantage_disadvantaged = request.form.get('rating_advantage_disadvantaged')
    rating_benefit_future = request.form.get('rating_benefit_future')
    rating_first_come = request.form.get('rating_first_come')
    rating_treatment_success = request.form.get('rating_treatment_success')
    rating_treatment_effort = request.form.get('rating_treatment_effort')
    rating_medication_effect = request.form.get('rating_medication_effect')
    rating_random_selection = request.form.get('rating_random_selection')

    conn = get_db_connection()
    conn.execute('''INSERT INTO procedural_ratings 
                    (save_life_years, advantage_disadvantaged, benefit_future, first_come, 
                     treatment_success, treatment_effort, medication_effect, random_selection) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                 (rating_save_life_years, rating_advantage_disadvantaged, rating_benefit_future, 
                  rating_first_come, rating_treatment_success, rating_treatment_effort, 
                  rating_medication_effect, rating_random_selection))
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
    gender = request.form.get('gender')
    age = request.form.get('age')
    religion = request.form.get('religion')
    other_religion = request.form.get('other_religion') if religion == 'other' else None

    conn = get_db_connection()
    conn.execute('INSERT INTO demography (gender, age, religion, other_religion) VALUES (?, ?, ?, ?)',
                 (gender, age, religion, other_religion))
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
    general_health = request.form.get('general_health')
    illness = request.form.get('illness')
    children = request.form.get('children')

    conn = get_db_connection()
    conn.execute('INSERT INTO group_preferences (general_health, illness, children) VALUES (?, ?, ?)',
                 (general_health, illness, children))
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
