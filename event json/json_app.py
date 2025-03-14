from flask import Flask, render_template, request, redirect, send_file, jsonify, flash
import json
import csv
import os
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

# Get the absolute path of the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'event_data.json')
CSV_FILE = os.path.join(BASE_DIR, 'events.csv')

# Initialize JSON file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)


def is_valid_email(email):
    """Basic email validation"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


@app.route('/')
def index():
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)
        events.sort(key=lambda x: datetime.fromisoformat(x['start_time']))
    except Exception as e:
        flash("Error loading events: " + str(e), "error")
        events = []
    return render_template('index.html', events=events)


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        try:
            with open(DATA_FILE, 'r') as f:
                events = json.load(f)

            guest_list = [email.strip() for email in request.form["guest_emails"].split(",")]
            invalid_emails = [email for email in guest_list if not is_valid_email(email)]

            if invalid_emails:
                flash(f"Invalid guest email(s): {', '.join(invalid_emails)}", "error")
                return redirect('/create_event')

            new_event = {
                "event_id": f"E{len(events)+1:03}",
                "event_name": request.form["event_name"],
                "event_type": request.form["event_type"],
                "start_time": request.form["start_time"],
                "duration_minutes": int(request.form["duration"]),
                "status": request.form["status"],
                "guest_emails": guest_list,
                "agenda": request.form["agenda"]
            }

            # Validate datetime format
            try:
                datetime.fromisoformat(new_event["start_time"])
            except ValueError:
                flash("Invalid date format. Use ISO format: YYYY-MM-DDTHH:MM", "error")
                return redirect('/create_event')

            events.append(new_event)

            # Save to JSON
            with open(DATA_FILE, 'w') as f:
                json.dump(events, f, indent=2)

            # Save to CSV
            if events:
                keys = events[0].keys()
                with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f_csv:
                    writer = csv.DictWriter(f_csv, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(events)

            flash("Event created successfully!", "success")
            return redirect('/')

        except Exception as e:
            flash("Error creating event: " + str(e), "error")
            return redirect('/create_event')

    return render_template('create_event.html')


@app.route('/download_csv')
def download_csv():
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)

        if not events:
            return "No events found to export as CSV.", 404

        if not os.path.exists(CSV_FILE):
            keys = events[0].keys()
            with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f_csv:
                writer = csv.DictWriter(f_csv, fieldnames=keys)
                writer.writeheader()
                writer.writerows(events)

        return send_file(CSV_FILE, as_attachment=True)

    except Exception as e:
        return f"Error downloading CSV: {e}", 500


@app.route('/api/events')
def get_events_json():
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)
        return jsonify(events)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
