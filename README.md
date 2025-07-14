Security CI/CD Pipeline Project


Overview

This project demonstrates an automated security-focused CI/CD pipeline that integrates security scanning directly into the development workflow. The system automatically scans code for vulnerabilities and blocks deployment if critical security issues are found.
What This Project Does
Automated Security Pipeline:
Monitors code changes in real-time
Automatically builds and deploys applications
Runs comprehensive security scans using industry-standard tools
Blocks deployment if vulnerabilities are detected
Generates detailed security reports
Provides real-time notifications and alerts

Key Security Features:

OWASP ZAP Integration - Automated web vulnerability scanning
Container Security - Scans Docker images for known vulnerabilities
Security Gates - Prevents insecure code from reaching production
Compliance Reporting - Generates security reports for audit purposes
Real-time Monitoring - Tracks security metrics and trends

Architecture
The pipeline consists of four main components running in Docker containers:

Jenkins - CI/CD orchestration and pipeline management
OWASP ZAP - Automated security vulnerability scanner
Vulnerable Application - Intentionally insecure web app for testing
PostgreSQL - Data persistence for Jenkins

All components communicate over a secure Docker network and include persistent storage for data retention.
Technologies Used

Docker & Docker Compose - Containerization and orchestration
Jenkins - CI/CD automation platform
OWASP ZAP - Security vulnerability scanner
Python Flask - Web application framework
PostgreSQL - Database for persistent storage
Git - Version control integration
