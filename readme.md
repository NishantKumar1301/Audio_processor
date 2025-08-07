# 🧩 VoiceLedger Project Setup Guide

This guide provides step-by-step instructions to set up and run the VoiceLedger project on your local machine.

---

## 📁 Clone the Repository

```bash
git clone https://github.com/NishantKumar1301/Audio_processor
cd your-django-project
```

---

## 🐍 Step 1: Create a Virtual Environment

### ▶ For Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### ▶ For Ubuntu / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### ▶ For macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Step 2: Install Required Packages

Make sure you're in the project root directory and run:

```bash
pip install -r requirements.txt
```

---

## 🔐 Step 3: Configure Environment Variables

Copy the example `.env` file:

```bash
cp .env.example .env
```

Then, open the `.env` file and fill in your credentials:

```env
API_KEY=your_api_key
SECRET_KEY=your_django_secret_key
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

> ⚠ Make sure `.env` is added to your `.gitignore` file to avoid exposing sensitive credentials.

---

## 🔄 Step 4: Apply Migrations

Generate and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🚀 Step 5: Run the Development Server

Start the local server:

```bash
python manage.py runserver
```

Visit your app at: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🛠 Optional: Create Superuser (Admin Login)

To access the Django admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

---

## ✅ You're All Set!

VoiceLedger project is now up and running. Happy coding! 🚀
