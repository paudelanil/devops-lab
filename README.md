# CI/CD with Jenkins, Docker, and Docker Compose

This project demonstrates a **CI/CD pipeline** using **Jenkins, Docker, and Docker Compose** to automate the build and deployment of a **full-stack application**.

## Project Structure
- `backend/` - Python backend with Flask.
- `database/` - MySQL database with initialization script.
- `frontend/` - React frontend.
- `Jenkinsfile` - Defines the Jenkins pipeline.
- `docker-compose.yml` - Manages multi-container deployment.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/your-project.git
cd your-project
```
### 2. Start Services

```bash
docker-compose up -d

```
### 4. Access Application 
FrontEnd: `http://localhost:3000`


