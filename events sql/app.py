from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/attachments'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MySQL connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor(dictionary=True)

# ------------------ Routes ------------------

@app.route('/')
@app.route('/create', methods=['GET', 'POST'])  # Default: create event page
def create_event():
    if request.method == 'POST':
        # Required fields
        title = request.form.get('title')
        date = request.form.get('date')
        time = request.form.get('time')
        guests = request.form.get('guests')
        meet_link = request.form.get('meet_link')

        if not all([title, date, time, guests, meet_link]):
            return "Missing required fields", 400
        if "meet.google.com" not in meet_link:
            return "Invalid Google Meet link", 400
        try:
            datetime.strptime(date, '%Y-%m-%d')
            datetime.strptime(time, '%H:%M')
        except ValueError:
            return "Invalid date or time format", 400

        # Optional fields
        description = request.form.get('description')
        duration = request.form.get('duration')
        location = request.form.get('location')

        # Attachment
        attachment_file = request.files.get('attachment')
        filename = None
        if attachment_file and attachment_file.filename != '':
            filename = secure_filename(attachment_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            attachment_file.save(file_path)

        # Insert into database
        query = """
            INSERT INTO events (title, description, date, time, duration, location, guests, meet_link, attachment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (title, description, date, time, duration, location, guests, meet_link, filename)
        try:
            cursor.execute(query, values)
            db.commit()
        except Exception as e:
            return f"Database error: {e}", 500

        return redirect(url_for('view_events'))

    return render_template('create_event.html')


@app.route('/events')
def view_events():
    try:
        cursor.execute("SELECT * FROM events ORDER BY date DESC, time DESC")
        events = cursor.fetchall()
    except Exception as e:
        return f"Error fetching events: {e}", 500
    return render_template('view_events.html', events=events)

# ------------------ Run App ------------------

if __name__ == '__main__':
    app.run(debug=True)

