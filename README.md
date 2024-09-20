# Interactive-Quiz-Application

![image](https://github.com/user-attachments/assets/95d1ba66-c0c7-4995-a7eb-380ecfc442bc)


This is an interactive quiz application built using Django. The application allows users to register, log in, and take quizzes. It features a responsive design and includes a homepage, login, registration, quiz, and results pages.

![GitHub repo size](https://img.shields.io/github/repo-size/senhorvance/Interactive-Quiz-Application)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/senhorvance/Interactive-Quiz-Application)
![GitHub Release](https://img.shields.io/github/v/release/senhorvance/Interactive-Quiz-Application)

## Features

- **User Authentication**: Users can sign up, log in, and log out.
- **Quiz Functionality**: Users can take quizzes with multiple-choice questions.
- **Real-Time Feedback**: The application shows correct answers with green ticks and incorrect answers with red crosses.
- **Responsive Design**: The front end is styled for a modern look and feel, and is responsive across different devices.

## Setup and Run

To set up and run the Interactive-Quiz-Application locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Interactive-Quiz-Application.git
   cd Interactive-Quiz-Application
   ```
2. **Create a virtual environment:**
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install the required dependencies:**
   ```bash
    pip install -r requirements.txt
   ```
4. **Set up the database:**
   ```bash
    python manage.py makemigrations
    python manage.py migrate
   ```
5. **Create a superuser (admin account):**
   ```bash
    python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
    python manage.py runserver
   ```
7. **Access the application:** Open your browser and go to `http://127.0.0.1:8000/` to see the homepage.

## Technologies Used
### Front-End
- HTML
- CSS
- Javascript
### Back-End
- Django (Python)
- SQLite (Database)

## Credits
- HTML/CSS/JS Template from [cruip.com](https://cruip.com/demos/solid/)
