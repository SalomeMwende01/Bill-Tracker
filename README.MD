# Purpose of the App

The Bill Tracker mobile app allows users to:

- Register and log in
- Create and manage expense groups
- Add shared expenses
- View balances and refunds
- Track settlements among group members

---

# Frontend

## Tech Stack

- React Native (Expo)
- JavaScript (JSX)
- Axios (API communication)
- Redux Toolkit (state management)
- React Navigation (navigation)
- Django REST API (backend)

---

## 📂 Folder Structure

bill-tracker-mobile/
│
├── App.jsx # App entry point
├── app.json # Expo configuration
├── package.json # Dependencies
├── babel.config.js
├── .env.example # Environment variables template
│
├── src/
│ ├── api/ # API communication with backend
│ ├── assets/ # Images and icons
│ ├── components/ # Reusable UI components
│ ├── navigation/ # Navigation setup
│ ├── screens/ # App screens
│ ├── store/ # Redux state management
│ ├── utils/ # Helper functions
│ ├── hooks/ # Custom hooks
│ └── theme/ # Colors, spacing, typography

---

## Install Dependencies

Ensure Node.js (v18+) is installed.
command - npm install

## Environment Variables

cp .env.example .env

Edit .env:
API_URL=http://localhost:8000/api

Do NOT commit .env files.

## Run the App

expo start

Scan the QR code using Expo Go
Or run on an emulator

---

# BACKEND

## Purpose of the Backend

The backend provides:

- User authentication
- Group and member management
- Expense recording
- Refund and settlement calculations
- Secure API endpoints for the mobile app

---

## Tech Stack

- Python 3.10+
- Django
- Django REST Framework
- SQLite3 (development database)
- JWT Authentication (SimpleJWT)

---

## Project Structure

billtracker_backend/
│
├── manage.py
├── requirements.txt
├── .env.example
│
├── config/ # Project configuration
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
│
├── apps/
│ ├── users/ # Authentication & user management
│ ├── groups/ # Group management
│ ├── expenses/ # Expense tracking
│ └── settlements/ # Refund calculations
│
└── media/ # Uploaded receipts

## Create Virtual Environment

python -m venv venv:

- source venv/bin/activate # Linux/Mac
- venv\Scripts\activate # Windows

## Install Dependencies

pip install -r requirements.txt

## Environment Variables

Create a .env file:

- cp .env.example .env

### Example .env:

DEBUG=True
SECRET_KEY=your-secret-key

## Run Migrations
python manage.py makemigrations
python manage.py migrate

## Start the Server

 - python manage.py runserver

API will be available at:

http://localhost:8000/


---

## Local Setup Instructions

### Clone the Repository

git clone https://github.com/your-username/Bill_Tracker.git
cd Bill_Tracker
