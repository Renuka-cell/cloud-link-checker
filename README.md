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
