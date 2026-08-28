# ☁️ Cloud-Based Link Monitoring & Reporting System

A cloud-based web application built with Django that automatically monitors website URLs, detects broken links, measures response time, generates monitoring reports, and provides a centralized dashboard for website health monitoring.

The system also supports automated URL monitoring using APScheduler, cloud-based report storage using Cloudinary, Google OAuth authentication, and production deployment using Render with PostgreSQL.

---

## 📌 Project Overview

The Cloud-Based Link Monitoring & Reporting System is designed to reduce the manual effort involved in checking website links.

Users can enter one or multiple URLs and monitor their availability, HTTP status, and response time through an interactive dashboard.

The system can automatically recheck stored URLs at fixed intervals and maintain monitoring history. Reports can be generated in CSV format and uploaded to Cloudinary for remote access and downloading.

The project combines web development, REST APIs, automation, authentication, databases, cloud storage, and cloud deployment into a single practical application.

---

## 🎯 Objectives

- Automatically monitor website URLs.
- Detect active and broken links.
- Measure website response time.
- Reduce false broken-link detection using retry logic.
- Provide a centralized monitoring dashboard.
- Automate repeated URL checking.
- Generate downloadable monitoring reports.
- Store reports using cloud storage.
- Provide secure user authentication.
- Deploy the application on a cloud platform.

---

## ✨ Key Features

### 🔗 URL Monitoring
- Check single or multiple website URLs.
- Validate URLs before monitoring.
- Detect active and broken links.
- Analyze HTTP response status.
- Calculate response time.

### 🔄 Retry Mechanism
- Failed requests are retried multiple times.
- The system retries approximately 2–3 times.
- Helps reduce false broken-link detection caused by temporary network or server issues.

### 📊 Monitoring Dashboard
- Total URLs monitored.
- Active and broken link statistics.
- Response time information.
- Recent monitoring activity.
- Monitoring history.
- Report management.

### ⏱️ Automated Monitoring
- APScheduler is used for automated monitoring.
- Stored URLs can be rechecked automatically at fixed intervals.
- Monitoring results are updated without requiring manual checking.

### 📄 CSV Reports
- Generate monitoring reports in CSV format.
- Reports contain URL, status, response time, and timestamp.
- Reports can be viewed and downloaded.

### ☁️ Cloud Storage
- Cloudinary is used to store generated reports.
- Provides remotely accessible report links.
- Supports report viewing, downloading, and deletion.

### 🔐 Authentication
- Username/password authentication.
- Login and logout functionality.
- Google OAuth authentication.
- User-specific monitoring information.

### 🖥️ User Interface
- Responsive web interface.
- Dashboard-based monitoring.
- Navigation system.
- Dark mode.
- Cookie consent.
- User profile display.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │    USER / BROWSER   │
                    │ Login / Dashboard   │
                    │ Monitor / Reports   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FRONTEND       │
                    │   HTML / CSS / JS   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      API LAYER      │
                    │    Django Ninja     │
                    │ /api/check/         │
                    │ /api/monitor-data/  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       BACKEND       │
                    │       Django        │
                    │ URL Validation      │
                    │ HTTP Requests       │
                    │ Status Detection    │
                    │ Response Time       │
                    │ Retry Mechanism     │
                    └──────┬─────┬─────┬──┘
                           │     │     │
             ┌─────────────┘     │     └─────────────┐
             ▼                   ▼                   ▼
     ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
     │   DATABASE   │    │    CLOUD     │    │  SCHEDULER   │
     │ PostgreSQL   │    │   Cloudinary │    │ APScheduler  │
     │              │    │ CSV Reports  │    │ Auto Monitor │
     └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
            │                   │                   │
            └───────────────────┴───────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │   DASHBOARD OUTPUT  │
                    │ Status / Response   │
                    │ Time / Reports      │
                    └─────────────────────┘
```

---

## 🔄 Application Workflow

1. User logs into the application.
2. User enters one or multiple URLs.
3. Frontend sends the URL data to the Django Ninja API.
4. API passes the request to the Django backend.
5. Backend validates the URL.
6. Backend sends an HTTP request to the target website using Python's `requests` library.
7. The response status and response time are analyzed.
8. Failed requests are retried approximately 2–3 times.
9. The URL is classified as active or broken.
10. Monitoring results are stored in the database.
11. APScheduler automatically rechecks URLs at configured intervals.
12. Monitoring data can be converted into CSV reports.
13. Reports can be uploaded to Cloudinary.
14. Dashboard displays monitoring statistics and reports.

---

## 🌐 HTTP Request Flow

The application uses two different HTTP communication flows.

### 1. Frontend → Backend API

The frontend sends an API request to Django Ninja.

```text
   Frontend
      ↓
POST /api/check/
      ↓
Django Ninja API
      ↓
Django Backend
      ↓
HTTP GET Request
      ↓
Target Website
      ↓
HTTP Response
      ↓
Backend analyzes response
```

### 2. Backend → Target Website

The Django backend sends the actual monitoring request to the target website.

    Django Backend
          ↓
    HTTP GET Request
          ↓
    Target Website
          ↓
    HTTP Response
          ↓
    Backend analyzes response

The backend checks:

- HTTP status code
- Availability
- Response time
- Connection and timeout errors

---

## 🧠 URL Monitoring Logic

The monitoring engine uses Python's `requests` library to send HTTP requests.

The general monitoring process is:

    URL Input
       ↓
    URL Validation
       ↓
    HTTP Request
       ↓
    Check Response
       ↓
    Successful?
     ┌───────┴───────┐
    Yes              No
     ↓                ↓
    Active        Retry Request
                      ↓
                 Retry 2–3 Times
                      ↓
                 Still Failed?
                  ┌────┴────┐
                 Yes        No
                  ↓          ↓
               Broken      Active

---

## 🔄 Retry Mechanism

The retry mechanism is primarily applied when a request fails or becomes unreachable.

Example:

    First Request  → Failed
    Second Attempt → Failed
    Third Attempt  → Failed
                         ↓
                    Mark as Broken

If a retry succeeds:

    Request → Successful
               ↓
           Mark Active

This reduces false broken-link detection caused by temporary network failures, timeouts, or temporary server problems.

---

## 🗄️ Database

### Local Development

SQLite is used during local development because it is lightweight and requires minimal configuration.

    Local Environment
           ↓
         SQLite

### Production Deployment

PostgreSQL is used for the deployed application.

    Render
       ↓
    PostgreSQL

PostgreSQL provides better support for production workloads, concurrent access, scalability, and cloud deployment.

### Database Configuration

The application uses `DATABASE_URL` as an environment variable for the production database connection.

Django uses `dj-database-url` to parse the PostgreSQL connection URL.

---

## 📦 Main Data Stored

The database stores information such as:

- User information
- Monitored URLs
- Link status
- Response time
- Monitoring timestamps
- Monitoring history
- Report information

---

## ⏱️ Scheduler

APScheduler is used to automate repeated URL monitoring.

Instead of requiring users to manually check URLs repeatedly, the scheduler triggers monitoring tasks at configured intervals.

    Scheduler
        ↓
    Monitoring Task
        ↓
    Check Stored URLs
        ↓
    Update Results
        ↓
    Database
        ↓
    Dashboard

---

## ☁️ Cloud Storage – Cloudinary

Cloudinary is integrated into the project for cloud-based report storage.

Generated CSV reports can be:

- Uploaded to Cloudinary
- Stored remotely
- Viewed
- Downloaded
- Deleted

This provides remote access to monitoring reports.

---

## 🔐 Authentication

The application supports two authentication methods.

### Traditional Authentication

- User registration
- Username/password login
- Logout
- Session management

### Google OAuth

Google OAuth is implemented using `django-allauth`.

The authentication flow is:

    User
     ↓
    Continue with Google
     ↓
    Google Authentication
     ↓
    OAuth Callback
     ↓
    Django
     ↓
    Authenticated User
     ↓
    Dashboard

Google OAuth credentials are stored securely using environment variables.

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Backend | Django |
| API | Django Ninja |
| Programming Language | Python |
| Frontend | HTML, CSS, JavaScript |
| Local Database | SQLite |
| Production Database | PostgreSQL |
| Cloud Storage | Cloudinary |
| Authentication | Django Allauth + Google OAuth |
| Scheduler | APScheduler |
| HTTP Requests | Python Requests |
| Static Files | WhiteNoise |
| Production Server | Gunicorn |
| Version Control | Git / GitHub |
| Cloud Deployment | Render |

---

## 📁 Project Structure

    linkchecker_project/
    │
    ├── checker/
    │   ├── migrations/
    │   ├── static/
    │   ├── templates/
    │   │   ├── base.html
    │   │   ├── dashboard.html
    │   │   ├── index.html
    │   │   ├── login.html
    │   │   ├── monitor.html
    │   │   ├── reports.html
    │   │   ├── signup.html
    │   │   └── view_report.html
    │   │
    │   ├── admin.py
    │   ├── api.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── monitor.py
    │   ├── tasks.py
    │   ├── tests.py
    │   └── views.py
    │
    ├── linkchecker_project/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    ├── staticfiles/
    ├── build.sh
    ├── manage.py
    ├── Procfile
    ├── requirements.txt
    ├── .gitignore
    └── README.md

---

## 🚀 Local Installation

### 1. Clone the Repository

    git clone https://github.com/Renuka-cell/cloud-link-checker.git

### 2. Open the Project Directory

    cd cloud-link-checker

### 3. Create a Virtual Environment

    python -m venv venv

### 4. Activate the Virtual Environment

#### Windows

    venv\Scripts\activate

#### Linux / macOS

    source venv/bin/activate

### 5. Install Dependencies

    pip install -r requirements.txt

### 6. Configure Environment Variables

Create a `.env` file in the project root.

Example:

    SECRET_KEY=your_django_secret_key
    DEBUG=True

    EMAIL_HOST_USER=your_email
    EMAIL_HOST_PASSWORD=your_email_password

    CLOUDINARY_CLOUD_NAME=your_cloudinary_cloud_name
    CLOUDINARY_API_KEY=your_cloudinary_api_key
    CLOUDINARY_API_SECRET=your_cloudinary_api_secret

    GOOGLE_CLIENT_ID=your_google_client_id
    GOOGLE_CLIENT_SECRET=your_google_client_secret

    DATABASE_URL=your_database_url

> **Important:** Never commit real credentials, API keys, passwords, OAuth secrets, or database credentials to GitHub.

### 7. Apply Migrations

    python manage.py makemigrations
    python manage.py migrate

### 8. Collect Static Files

    python manage.py collectstatic --noinput

### 9. Run the Development Server

    python manage.py runserver

Open the application at:

    http://127.0.0.1:8000/

---

## ☁️ Cloud Deployment

The application is deployed using the Render cloud platform.

### Production Architecture

    GitHub Repository
           ↓
         Render
           ↓
    Django Application
           ↓
    PostgreSQL Database
           ↓
    Cloudinary Storage

### Deployment Components

The deployment uses:

- Render Web Service
- Render PostgreSQL
- Gunicorn
- WhiteNoise
- Environment variables
- Django migrations
- Static file collection

### Build Command

    pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

### Start Command

    gunicorn linkchecker_project.wsgi:application

---

## 🔑 Environment Variables

The following environment variables are required for the application configuration:

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Django security key |
| `DEBUG` | Django debug configuration |
| `ALLOWED_HOSTS` | Allowed production hosts |
| `EMAIL_HOST_USER` | Email service username |
| `EMAIL_HOST_PASSWORD` | Email service password |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret |
| `DATABASE_URL` | PostgreSQL database connection |

---

## 🔒 Security Considerations

Sensitive information is not stored directly in the source code.

Environment variables are used for:

- Django secret key
- Database credentials
- Google OAuth credentials
- Cloudinary credentials
- Email credentials

The `.env` file should remain local and must be included in `.gitignore`.

---

## 📊 Dashboard

The monitoring dashboard provides:

- Total monitored URLs
- Active links
- Broken links
- Response time
- Monitoring history
- Recent activity
- Cloud reports
- Download and delete options

---

## 📄 Report Generation

The system generates CSV reports containing monitoring information such as:

    URL
    Status
    Response Time
    Timestamp

Reports can be downloaded locally or uploaded to Cloudinary for cloud storage.

---

## ⚠️ Challenges Faced

### 1. Database Integration

SQLite was suitable for local development, while PostgreSQL was integrated for production cloud deployment.

**Solution:**

Implemented environment-based database configuration using `DATABASE_URL` and `dj-database-url`.

### 2. Environment Variable Management

Sensitive credentials should not be hardcoded.

**Solution:**

Moved sensitive configuration to environment variables and configured them in Render.

### 3. Static File Handling

Django static files required additional configuration in production.

**Solution:**

Configured WhiteNoise and `collectstatic` during deployment.

### 4. Google OAuth Configuration

OAuth requires correct production callback and redirect configuration.

**Solution:**

Configured the deployed Render URL and OAuth credentials correctly.

### 5. Scheduler in Cloud Environment

Background scheduler execution can be affected by cloud service lifecycle and resource limitations.

**Solution:**

Controlled scheduler execution and optimized monitoring intervals.

### 6. Deployment Configuration

The project initially encountered deployment and path configuration issues.

**Solution:**

Corrected the repository structure, Render configuration, build commands, database configuration, and Gunicorn startup command.

---

## 🌐 Live Application

**Live Demo:**

https://linkchecker-project.onrender.com

> The application may experience availability limitations depending on the Render service plan and cloud instance lifecycle.

---

## 📂 GitHub Repository

**Source Code:**

https://github.com/Renuka-cell/cloud-link-checker

---

## 🎓 Project Type

This project was developed as an academic mini project under the Cloud Computing specialization.

It demonstrates practical implementation of:

- Cloud Computing
- Web Development
- REST APIs
- Database Management
- Cloud Storage
- Authentication
- Automation
- Cloud Deployment

---

## 🔮 Future Enhancements

Possible future improvements include:

- Email notifications for broken links
- Advanced website health analytics
- Response-time graphs and historical trends
- Celery/Redis-based background task processing
- Improved scheduler architecture for large-scale monitoring
- PostgreSQL optimization for large datasets
- Role-based administration
- Docker-based deployment
- Monitoring alerts and notifications
- Support for multiple cloud deployment platforms

---

## 👩‍💻 Author

**Renuka Balaji Biradar**

Computer Science & Engineering

**GitHub:**

https://github.com/Renuka-cell

**LinkedIn:**

https://www.linkedin.com/in/renuka-biradar-782100273/

---

## 📜 License

This project was developed for academic and educational purposes.
