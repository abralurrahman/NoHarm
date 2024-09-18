from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home route to display survey
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
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

        return redirect('/')
    return 'Survey submission failed'

# Route to view survey results
@app.route('/results')
def results():
    conn = get_db_connection()
    surveys = conn.execute('SELECT * FROM survey').fetchall()
    conn.close()
    return render_template('results.html', surveys=surveys)

if __name__ == '__main__':
    app.run(debug=True)
