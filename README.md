# 📅 Event Management Web App

This is a lightweight, user-friendly **Event Management Application** built with **Flask** and backed by **MySQL**. It allows users to create, view, and manage events with features like Google Meet link validation, guest email capture, file attachments, and a responsive frontend.
## 🚀 Features
- ✅ Create and manage events
- 📧 Add multiple guest emails
- 🔗 Validates Google Meet links
- 📁 Upload and store file attachments
- 🗓️ View all created events in a sorted list
- 🛡️ Secured credentials using `.env` file
- 🖥️ Responsive UI with Jinja2 templating

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Database:** MySQL
- **Frontend:** HTML5, CSS3 (Jinja templates)
- **Other:** dotenv, MySQL Connector, Werkzeug

## 📷 Screenshots
![image](https://github.com/user-attachments/assets/4e2998e4-5fe4-4098-84af-27703efb22f8)
![image](https://github.com/user-attachments/assets/3066e992-33ca-44ef-b0bc-160f5abf723b)

## 📁 Folder Structure
├── app.py ├── .env # Environment variables (not tracked in Git) ├── .gitignore 
├── templates/ │ ├── index.html │ └── events.html 
├── uploads/ # For file attachments

## 🧪 How to Run Locally
1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Set up a virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
or
source venv/bin/activate   # On macOS/Linux

3. Install the required packages
pip install -r requirements.txt

4. Set up your MySQL database
Create a database (e.g., event_manager) and run the following SQL:
You can use MySQL CLI or a GUI like MySQL Workbench

CREATE TABLE events (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  date DATE NOT NULL,
  time TIME NOT NULL,
  location VARCHAR(255) NOT NULL,
  meet_link VARCHAR(255),
  guest_emails TEXT,
  attachment VARCHAR(255)
);

5. Create a .env file in the root folder with the following variables
DB_HOST=localhost
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=event_manager

6. Run the Flask app
app.py

7. Open in your browser
Visit: http://localhost:5000/

💡 Future Enhancements
✅ Add search & filter to events
✅ Pagination support
✅ Admin panel
✅ RSVP system for guests

🤝 Contributing
Contributions, suggestions, and issues are welcome!

📄 License
This project is open-source and available under the MIT License.
