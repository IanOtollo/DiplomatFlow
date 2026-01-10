# DiplomatFlow - MOFA Task Tracker

A comprehensive web-based task management and ICT equipment tracking system designed for the Ministry of Foreign Affairs (MOFA). This Django-powered application enables officers and attachés to digitally record tasks, track ICT equipment, monitor device assignments, and generate detailed reports with full accountability and audit trails.

![Django](https://img.shields.io/badge/Django-4.2.27-green.svg)
![Python](https://img.shields.io/badge/Python-3.9.23-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Task Management
- **Digital Task Recording**: Officers and attachés can record tasks with date and time stamps
- **Task Assignment**: Assign tasks to specific users or directorates
- **Priority & Status Tracking**: Categorize tasks by priority (Low, Medium, High, Urgent) and status (Pending, In Progress, Completed, Cancelled, On Hold)
- **Task Categories**: Organize tasks by category (Administrative, Consular, Protocol, Economic, Political, Legal, Security, IT, Finance, HR, Other)
- **Task Editing & Deletion**: Edit and delete tasks with confirmation prompts for accountability
- **Task Comments**: Add comments and attachments to tasks
- **Due Date Management**: Set and track due dates with overdue notifications
- **Time Tracking**: Record estimated and actual minutes spent on tasks
- **Room/Office Tracking**: Associate tasks with specific room numbers

### ICT Equipment Management
- **Equipment Registration**: Record new ICT equipment purchased for the ministry
- **Equipment Types**: Support for laptops, desktops, tablets, printers, scanners, monitors, routers, servers, phones, projectors, and more
- **Device Assignment**: Assign devices to directorates (e.g., Peace & Security, AU, Asia) or individual officers
- **Assignment Tracking**: Track which ICT officer issued a device and to which office
- **Device History**: Maintain complete history of device movement across rooms and directorates
- **Condition Monitoring**: Track device condition (Excellent, Good, Fair, Poor, Needs Repair, Decommissioned)
- **Issue Reporting**: Report device problems with severity levels (Low, Medium, High, Critical)
- **Issue Resolution**: Track issue resolution with notes and timestamps
- **Recurring Problem Detection**: Automatically identify recurring problems in directorates and suggest solutions
- **Real-time Tracking**: Real-time tracking of devices issued to directorates
- **Location Monitoring**: Monitor responsible officers and device locations

### User Management
- **Custom User Model**: Extended user model with department, phone number, and profile information
- **Secure Authentication**: Secure login and logout system for accountability
- **User Profiles**: User profile management with profile pictures
- **Department Organization**: Organize users by departments (Administration, Diplomacy, Consular, Protocol, Security, Finance, HR, IT, Legal, Media, Other)
- **Password Reset**: Admin-controlled password reset system with request tracking
- **User Roles**: Support for different user roles and permissions

### Reporting & Analytics
- **Task Analytics**: Comprehensive task analytics and statistics
- **Team Performance**: Team performance reports and metrics
- **Monthly Reports**: Generate monthly reports for tasks and equipment
- **Data Export**: Export data in various formats
- **Dashboard Views**: Interactive dashboards for tasks and equipment

### User Interface
- **Modern Dark Theme**: Beautiful dark theme inspired by modern design trends
- **Responsive Design**: Fully responsive design that works on all devices
- **Animations**: Smooth animations and transitions throughout the application
- **Full-Width Layout**: Content spans the entire viewport for optimal viewing
- **Glassmorphism Effects**: Modern glassmorphism UI elements
- **Gradient Backgrounds**: Animated gradient backgrounds and orbs
- **Accessibility**: Accessible design with proper contrast and navigation

## 🛠 Technology Stack

### Backend
- **Django 4.2.27**: High-level Python web framework
- **Python 3.9.23**: Programming language
- **SQLite**: Default database (can be configured for PostgreSQL/MySQL)

### Frontend
- **Bootstrap 5**: Frontend framework for responsive design
- **Crispy Forms**: Django package for rendering forms
- **Font Awesome**: Icon library
- **Custom CSS**: Custom styling with CSS variables and animations
- **JavaScript**: Interactive features and animations

### Additional Packages
- **django-allauth**: Authentication and account management
- **django-crispy-forms**: Form rendering
- **django-tables2**: Table rendering
- **django-environ**: Environment variable management
- **django-celery-beat**: Periodic task scheduling
- **django-celery-results**: Celery result backend
- **django-compressor**: Static file compression
- **django-cors-headers**: CORS handling
- **django-debug-toolbar**: Development debugging
- **django-timezone-field**: Timezone field support
- **Pillow**: Image processing
- **reportlab**: PDF generation
- **whitenoise**: Static file serving
- **gunicorn**: WSGI HTTP server

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd DiplomatFlow
```

### Step 2: Create Virtual Environment
```bash
python -m venv myenv
# On Windows
myenv\Scripts\activate
# On Linux/Mac
source myenv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root (optional, defaults are provided):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Collect Static Files
```bash
python manage.py collectstatic
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## ⚙️ Configuration

### Database Configuration
By default, the application uses SQLite. To use PostgreSQL or MySQL, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Email Configuration
Update email settings in `settings.py` for production:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Security Settings
For production, ensure:
- `DEBUG = False`
- Set a strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Enable SSL/HTTPS
- Use secure cookies

## 📖 Usage

### Accessing the Application
1. Navigate to `http://127.0.0.1:8000/`
2. Login with your superuser credentials or create a new account
3. Access the dashboard to view tasks and equipment

### Creating Tasks
1. Navigate to **Tasks** → **Create Task**
2. Fill in task details (title, description, category, priority, due date)
3. Assign to a user or directorate
4. Save the task

### Managing Equipment
1. Navigate to **Equipment** → **Add Equipment**
2. Enter equipment details (type, brand, model, serial number)
3. Record purchase information
4. Assign equipment to directorates or officers

### Assigning Devices
1. Navigate to **Equipment** → **Assignments** → **Create Assignment**
2. Select equipment and directorate
3. Specify room number and assignment details
4. The system automatically tracks the assignment history

### Reporting Issues
1. Navigate to **Equipment** → **Report Issue**
2. Select the equipment with the issue
3. Describe the problem and set severity
4. Track resolution status

### Generating Reports
1. Navigate to **Reports** → Select report type
2. Configure filters and date ranges
3. Generate and export reports

## 📁 Project Structure

```
DiplomatFlow/
├── mofa_task_tracker/          # Main project directory
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py                 # WSGI configuration
│   └── asgi.py                 # ASGI configuration
├── users/                       # User management app
│   ├── models.py               # CustomUser model
│   ├── views.py                # User views
│   ├── forms.py                # User forms
│   └── urls.py                 # User URLs
├── tasks/                       # Task management app
│   ├── models.py               # Task, TaskComment, TaskAttachment models
│   ├── views.py                # Task views
│   ├── forms.py                # Task forms
│   └── urls.py                 # Task URLs
├── equipment/                   # ICT Equipment management app
│   ├── models.py               # Equipment, Assignment, History, Issue models
│   ├── views.py                # Equipment views
│   ├── forms.py                # Equipment forms
│   └── urls.py                 # Equipment URLs
├── reports/                     # Reporting app
│   ├── views.py                # Report views
│   └── urls.py                 # Report URLs
├── home/                        # Homepage app
│   ├── views.py                # Home views
│   └── urls.py                 # Home URLs
├── templates/                   # HTML templates
│   ├── base/                   # Base templates
│   ├── tasks/                  # Task templates
│   ├── equipment/              # Equipment templates
│   ├── users/                  # User templates
│   └── reports/                # Report templates
├── static/                      # Static files
│   ├── css/                    # Stylesheets
│   ├── js/                     # JavaScript files
│   └── img/                    # Images
├── media/                       # User-uploaded files
├── requirements.txt             # Python dependencies
├── manage.py                    # Django management script
├── Procfile                     # Heroku deployment configuration
├── runtime.txt                  # Python version specification
└── README.md                    # This file
```

## 🚢 Deployment

### Heroku Deployment
1. Create a Heroku app
2. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
   ```
3. Deploy:
   ```bash
   git push heroku main
   ```

### Azure Deployment
The application is configured for Azure App Service. Update `ALLOWED_HOSTS` in `settings.py` with your Azure domain.

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "mofa_task_tracker.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write docstrings for functions and classes
- Add tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Development Team** - Initial work

## 🙏 Acknowledgments

- Django community for excellent documentation
- Bootstrap team for the responsive framework
- All contributors who have helped improve this project

## 📞 Support

For support, please open an issue in the repository or contact the development team.

## 🔄 Version History

- **v1.0.0** - Initial release with task management and ICT equipment tracking
  - Task recording with timestamps
  - Equipment management
  - Device assignment tracking
  - Issue reporting and resolution
  - Recurring problem detection
  - Secure authentication
  - Comprehensive reporting

---

**Note**: This application is designed for use within the Ministry of Foreign Affairs. Ensure proper security measures are in place before deploying to production.

