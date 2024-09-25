from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'  # Secret key need to be added for session management

# Connect to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route to display the intro page
@app.route('/')
def intro():
    return render_template('intro.html')

# Route to display the survey form
@app.route('/survey')
def survey():
    return render_template('survey.html')

# Route to handle form submission and redirect to thank you page
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        consent = request.form.get('consent')
        patient_choice = request.form.get('patient_choice')
        procedure_rating = request.form.getlist('procedure_rating')
        age = request.form.get('age')
        gender = request.form.get('gender')
        religion = request.form.get('religion')

        conn = get_db_connection()
        conn.execute('INSERT INTO survey (consent, patient_choice, procedure_rating, age, gender, religion) VALUES (?, ?, ?, ?, ?, ?)',
                     (consent, patient_choice, ','.join(procedure_rating), age, gender, religion))
        conn.commit()
        conn.close()

        return redirect('/thank-you')
    return 'Survey submission failed'

# Route to thank users after survey submission
@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

# Route for admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'admin':  # Admin password
            session['admin'] = True
            return redirect('/results')
        else:
            return "Incorrect password. Try again."
    return render_template('admin_login.html')

# Route to view survey results (admin only)
@app.route('/results')
def results():
    if 'admin' in session:  # Check if user is logged in as admin
        conn = get_db_connection()
        surveys = conn.execute('SELECT * FROM survey').fetchall()
        conn.close()
        return render_template('results.html', surveys=surveys)
    else:
        return redirect('/admin')  # Redirect to login page if not an admin

# Route to logout admin
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
