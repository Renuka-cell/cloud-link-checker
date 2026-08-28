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
