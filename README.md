# IPEC Django Project

A Django web application project with modern setup and best practices.

## Features

- Django 4.2+ framework
- Bootstrap 5 for responsive UI
- SQLite database (development)
- Environment configuration with python-decouple
- Static and media files management
- Admin interface
- Modern project structure

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone or download this project
2. Navigate to the project directory:
   ```bash
   cd IPEC
   ```

3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Copy the environment file:
   ```bash
   copy env.example .env
   ```
   (On macOS/Linux: `cp env.example .env`)

7. Run database migrations:
   ```bash
   python manage.py migrate
   ```

8. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

9. Start the development server:
   ```bash
   python manage.py runserver
   ```

10. Open your browser and visit `http://127.0.0.1:8000/`

## Project Structure

```
IPEC/
├── ipec/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py      # Django settings
│   ├── urls.py          # Main URL configuration
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── core/                # Core app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/           # HTML templates
│   ├── base.html
│   └── core/
│       ├── home.html
│       └── about.html
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploaded files
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── env.example          # Environment variables template
└── README.md           # This file
```

## Development

### Adding New Apps

1. Create a new app:
   ```bash
   python manage.py startapp app_name
   ```

2. Add the app to `INSTALLED_APPS` in `ipec/settings.py`

3. Create URL patterns in the app's `urls.py`

4. Include the app URLs in the main `ipec/urls.py`

### Database

The project uses SQLite by default for development. To use a different database:

1. Update the `DATABASES` setting in `ipec/settings.py`
2. Install the appropriate database adapter
3. Update `requirements.txt` with the new dependency

### Static Files

Static files are served from the `static/` directory. In production, you'll need to configure your web server to serve these files.

### Media Files

User-uploaded files are stored in the `media/` directory. Make sure to configure your web server to serve these files in production.

## Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in your environment variables
2. Set a secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` with your domain
4. Set up a production database
5. Configure static and media file serving
6. Set up proper logging
7. Use environment variables for sensitive settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).
