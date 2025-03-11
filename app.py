from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
import os
import mysql.connector
import re
from dotenv import load_dotenv

# ✅ Load .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'

# ✅ Create uploads folder if missing
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ✅ Connect to MySQL
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor(dictionary=True)

# ✅ Meet link validation
def is_valid_meet_link(link):
    return re.match(r'^https://meet\.google\.com/[a-z]{3}-[a-z]{4}-[a-z]{3}$', link)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/create_event', methods=['POST'])
def create_event():
    title = request.form['title']
    description = request.form['description']
    date = request.form['date']
    time = request.form['time']
    duration = request.form['duration']
    location = request.form['location']
    guests = request.form['guests']
    meet_link = request.form['meet_link']
    reminder = request.form['reminder']

    if not is_valid_meet_link(meet_link):
        return "❌ Invalid Google Meet link", 400

    guest_list = [email.strip() for email in guests.split(',')]
    for email in guest_list:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return f"❌ Invalid guest email: {email}", 400
    guests_str = ', '.join(guest_list)

    file = request.files['attachment']
    filename = None
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    insert_query = """
        INSERT INTO events (title, description, date, time, duration, location, guests, meet_link, reminder, attachment)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        title, description, date, time, duration, location, guests_str, meet_link, reminder, filename
    ))
    db.commit()

    return redirect(url_for('view_events'))

@app.route('/events')
def view_events():
    cursor.execute("SELECT * FROM events ORDER BY created_at DESC")
    events = cursor.fetchall()
    return render_template('events.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)
