# Mergington High School Activities Management System

A comprehensive web application built with FastAPI and MongoDB that allows students to view and sign up for extracurricular activities, with teacher authentication and management capabilities.

## Features

### Student Features
- **View Activities**: Browse all available extracurricular activities with detailed information
- **Advanced Filtering**: Filter activities by category (Sports, Arts, Academic, Community, Technology), day of the week, and time of day
- **Search Functionality**: Search activities by name or description
- **Activity Details**: View comprehensive information including schedules, participant limits, and current enrollment
- **Responsive Design**: Mobile-friendly interface with modern styling

### Teacher Features (Authentication Required)
- **Secure Login**: Teacher authentication system with hashed passwords
- **Student Registration**: Register students for activities on their behalf
- **Student Removal**: Remove students from activities when needed
- **Activity Management**: Monitor and manage activity participation

### Technical Features
- **RESTful API**: Full FastAPI backend with automatic API documentation
- **Database Integration**: MongoDB for persistent data storage
- **Security**: Argon2 password hashing and session-based authentication
- **Real-time Updates**: Dynamic content loading and form validation
- **Cross-platform**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Database**: MongoDB with PyMongo driver
- **Authentication**: Argon2 password hashing
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Server**: Uvicorn ASGI server
- **Development**: Hot reload support for rapid development

## API Endpoints

### Activities
- `GET /activities/` - Get all activities with optional filtering
  - Query parameters: `day`, `start_time`, `end_time`
- `GET /activities/days` - Get list of all available activity days
- `POST /activities/{activity_name}/signup` - Register a student for an activity (requires teacher auth)
- `POST /activities/{activity_name}/unregister` - Remove a student from an activity (requires teacher auth)

### Authentication
- `POST /auth/login` - Teacher login with username and password
- `GET /auth/check-session` - Validate teacher session

### Static Files
- `GET /` - Main application interface (redirects to `/static/index.html`)
- `GET /static/*` - Serve static frontend files
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Database Schema

### Activities Collection
- **_id**: Activity name (unique identifier)
- **description**: Detailed activity description
- **schedule**: Human-readable schedule string
- **schedule_details**: Structured schedule data with days, start_time, end_time
- **max_participants**: Maximum number of students allowed
- **participants**: Array of student email addresses

### Teachers Collection
- **_id**: Username (unique identifier)
- **display_name**: Full display name
- **password**: Argon2 hashed password
- **role**: Teacher role (teacher/admin)

## Sample Activities

The system comes pre-loaded with diverse activities including:
- **Sports**: Soccer Team, Basketball Team, Morning Fitness
- **Academic**: Math Club, Science Olympiad, Debate Team
- **Arts**: Art Club, Drama Club
- **Technology**: Programming Class, Weekend Robotics Workshop
- **Community**: Chess tournaments and competitions

## Authentication System

### Default Teacher Accounts
- **Username**: `mrodriguez` | **Password**: `art123` | **Role**: Teacher (Ms. Rodriguez)
- **Username**: `mchen` | **Password**: `chess456` | **Role**: Teacher (Mr. Chen)  
- **Username**: `principal` | **Password**: `admin789` | **Role**: Admin (Principal Martinez)

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).

### Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Ensure MongoDB is running locally on port 27017
3. Start the application: `uvicorn app:app --reload`
4. Access the application at `http://localhost:8000`
5. View API documentation at `http://localhost:8000/docs`

## Project Structure

```
src/
├── app.py                 # Main FastAPI application and configuration
├── requirements.txt       # Python dependencies
├── backend/
│   ├── database.py       # MongoDB connection and data initialization
│   └── routers/
│       ├── activities.py # Activity management endpoints
│       └── auth.py       # Authentication endpoints
└── static/
    ├── index.html        # Main web interface
    ├── app.js           # Frontend JavaScript logic
    └── styles.css       # Application styling
```
