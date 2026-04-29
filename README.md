# NSRIT College Feedback System

A comprehensive web-based feedback collection system built with **Flask** and **Python** for NSRIT College, supporting multiple engineering branches and semesters.

## Features

✅ **Multi-Branch Support**
- 7 Engineering Branches: CSE, CSE-AI&ML, CSE-DS, ECE, EEE, Mechanical, Civil
- Semester-wise (1-8) subject mapping
- Dynamic subject loading

✅ **User Roles**
- Student: Submit feedback, view complaints
- Admin: View analytics, manage complaints, filter feedback

✅ **Feedback System**
- Subject-wise feedback forms
- Faculty-wise feedback
- Lab and project feedback
- Rating system (1-5 scale)
- Multiple evaluation criteria

✅ **Complaint System**
- Student complaint submission
- Admin complaint management
- Status tracking (Pending/Resolved)

✅ **Analytics Dashboard**
- Faculty-wise average ratings
- Subject-wise feedback analysis
- Complaint tracking
- Real-time statistics

## Technology Stack

- **Backend**: Python 3.11 + Flask 2.3.3
- **Database**: SQLite (lightweight, no setup required)
- **Frontend**: Bootstrap 5 + HTML/CSS/JavaScript
- **Authentication**: Flask-Login + Werkzeug (password hashing)
- **Deployment**: Free hosting (Render, Railway, or Heroku)

## Local Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

1. **Clone/Download the project**
```bash
cd feedback-system
```

2. **Create virtual environment**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Seed the database**
```bash
python seed.py
```

5. **Run the application**
```bash
python run.py
```

6. **Access the application**
Open your browser and go to: `http://localhost:5000`

## Demo Credentials

### Student Login
- **Email**: Create new account (register as student)
- **Branch**: Select from dropdown
- **Semester**: 1-8

### Admin Login
- **Email**: admin@nsrit.edu
- **Password**: admin123

## Deployment (Free Hosting)

### Option 1: Render (Recommended)
1. Push code to GitHub
2. Create account at https://render.com
3. New → Web Service → Connect GitHub repo
4. Environment: Python
5. Build command: `pip install -r requirements.txt && python seed.py`
6. Start command: `gunicorn run:app`
7. Add environment variable: `SECRET_KEY=your-secret-key`

### Option 2: Railway
1. Install Railway CLI
2. Create account at https://railway.app
3. Connect GitHub repo
4. Set environment variables
5. Deploy automatically

### Option 3: Heroku (Limited Free Tier)
1. Install Heroku CLI
2. `heroku create your-app-name`
3. `git push heroku main`
4. Deploy with `Procfile` included

## Project Structure

```
feedback-system/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms validation
│   ├── auth.py              # Authentication routes
│   ├── student.py           # Student routes
│   ├── admin.py             # Admin routes
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── student/
│   │   └── admin/
│   └── static/              # CSS & JS
├── run.py                   # Entry point
├── seed.py                  # Database seeder
├── requirements.txt         # Dependencies
├── Procfile                 # Deployment config
└── .env                     # Environment variables
```

## Database Schema

### Core Models
- **User**: Authentication (email, password, role)
- **Student**: Student profile (roll_number, branch, semester)
- **Branch**: Engineering branches
- **Subject**: Semester-wise subjects by branch
- **Faculty**: Faculty information
- **Feedback**: Student feedback records
- **Complaint**: Student complaints

## API Routes

### Authentication
- `POST /register` - New user registration
- `POST /login` - User login
- `GET /logout` - Logout

### Student
- `GET /student/dashboard` - View subjects
- `POST /student/feedback/<id>` - Submit feedback
- `POST /student/complaint` - Submit complaint
- `GET /student/my-complaints` - View complaints

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/feedbacks` - View all feedbacks
- `GET /admin/complaints` - View complaints
- `POST /admin/complaint/<id>/resolve` - Resolve complaint
- `GET /admin/analytics` - Analytics dashboard

## Customization

### Add New Subject
Edit `seed.py` and add to `SUBJECTS_DATA` dictionary

### Change Branches
Modify `BRANCHES_DATA` in `seed.py`

### Customize Feedback Questions
Edit feedback form in `app/templates/student/feedback_form.html`

## Future Enhancements

- Export feedback reports (PDF/CSV)
- Email notifications
- SMS alerts
- Mobile app
- Advanced analytics charts
- Real-time notifications
- Multi-language support

## Support

For issues or questions, contact: admin@nsrit.edu

---

**Built with ❤️ for NSRIT College**
