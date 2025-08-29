# Student Management System

A FastAPI-based backend system for managing students and their grades with authentication, database integration, and comprehensive CRUD operations.

## 🚀 Features

- **Student Management**: Complete CRUD operations for student records
- **Grade Tracking**: Store and manage student grades as lists
- **JWT Authentication**: Secure endpoints with token-based authentication
- **Database Integration**: SQLModel with SQLite for data persistence
- **Request Logging**: Middleware to log all API requests
- **CORS Support**: Configured for frontend integration
- **Input Validation**: Pydantic models for data validation
- **Email Validation**: Unique email constraints with proper validation

## 📋 Requirements

- Python 3.8+
- FastAPI
- SQLModel
- SQLAlchemy
- Pydantic
- python-jose (JWT handling)
- passlib (password hashing)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd KodeCampTask7
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt.txt
   ```

3. **Run the application**
   ```bash
   uvicorn Student_Management_System.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, access the interactive API documentation:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Authentication

### Default Users

The system comes with pre-configured users in `users.json`:

| Username | Password   | Role    | Email              |
|----------|------------|---------|-------------------|
| admin    | admin123   | Admin   | admin@admin.com   |
| teacher  | teacher123 | Teacher | teacher@teacher.com |

### Getting Access Token

1. **Login Endpoint**: `POST /auth/token`
   ```bash
   curl -X POST "http://localhost:8000/auth/token" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin&password=admin"
   ```

2. **Response**:
   ```json
   {
     "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
     "token_type": "bearer"
   }
   ```

3. **Using the Token**:
   ```bash
   curl -X POST "http://localhost:8000/students/" \
        -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"name": "John Doe", "age": 20, "email": "john@example.com", "grades": [85.5, 92.0]}'
   ```

## 📖 API Endpoints

### Authentication Endpoints

| Method | Endpoint     | Description           | Auth Required |
|--------|-------------|-----------------------|---------------|
| POST   | `/auth/token` | Login and get token   | No            |

### Student Endpoints

| Method | Endpoint           | Description              | Auth Required |
|--------|--------------------|--------------------------|---------------|
| POST   | `/students/`       | Create a new student     | Yes           |
| GET    | `/students/`       | Get all students (paginated) | No        |
| GET    | `/students/{id}`   | Get student by ID        | No            |
| PUT    | `/students/{id}`   | Update student           | Yes           |
| DELETE | `/students/{id}`   | Delete student           | Yes           |

### Student Model

```json
{
  "id": 1,
  "name": "John Doe",
  "age": 20,
  "email": "john@example.com",
  "grades": [85.5, 92.0, 78.3]
}
```

## 💡 Usage Examples

### Create a Student
```bash
curl -X POST "http://localhost:8000/students/" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Alice Smith",
       "age": 22,
       "email": "alice@example.com",
       "grades": [88.5, 91.2, 87.8]
     }'
```

### Get All Students
```bash
curl -X GET "http://localhost:8000/students/?skip=0&limit=10"
```

### Get Student by ID
```bash
curl -X GET "http://localhost:8000/students/1"
```

### Update Student
```bash
curl -X PUT "http://localhost:8000/students/1" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Alice Johnson",
       "grades": [90.0, 93.5, 89.2]
     }'
```

### Delete Student
```bash
curl -X DELETE "http://localhost:8000/students/1" \
     -H "Authorization: Bearer YOUR_TOKEN"
```

## 🏗️ Project Structure

```
Student_Management_System/
├── main.py                 # FastAPI application entry point
├── auth.py                 # Authentication logic
├── utils.py                # Utility functions and middleware
├── database_setup.py       # Database configuration
├── users.json             # User credentials storage
├── models/
│   ├── student.py         # Student SQLModel
│   └── user.py            # User model
├── schemas/
│   ├── student.py         # Pydantic schemas for students
│   └── auth.py            # Authentication schemas
├── routers/
│   ├── student.py         # Student endpoints
│   └── auth.py            # Authentication endpoints
└── crud/
    └── student.py         # Database operations
```

## 🔧 Configuration

### Database
- **Type**: SQLite
- **File**: `students.db` (created automatically)
- **ORM**: SQLModel (built on SQLAlchemy)

### Security
- **Algorithm**: HS256
- **Token Expiration**: 30 minutes
- **Password Hashing**: bcrypt

### CORS
- **Allowed Origins**: `http://localhost:3000`
- **Credentials**: Enabled
- **Methods**: All
- **Headers**: All

### Logging
- **File**: `requests.log`
- **Format**: Timestamp, method, URL, status code, processing time
- **Level**: INFO

## 🚦 Development

### Running in Development Mode
```bash
uvicorn Student_Management_System.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing Authentication
```python
# Run the test script
python -m Student_Management_System.test_auth
```

### Adding New Users
Edit `users.json` and add new user entries with hashed passwords:
```json
{
  "username": "newuser",
  "hashed_password": "$2a$12$...",
  "email": "newuser@example.com",
  "is_active": true
}
```

## 📝 Logging

All requests are automatically logged to `requests.log` with the following format:
```
2024-01-15 10:30:45,123 - Student_Management_System.utils - INFO - Request POST http://localhost:8000/students/ 201 took 0.15 seconds
```

## 🛡️ Security Features

- **JWT Token Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **Email Uniqueness**: Prevents duplicate email addresses
- **Input Validation**: Pydantic models validate all input data
- **CORS Protection**: Configured for specific frontend origin

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request



## 🆘 Troubleshooting

### Common Issues

1. **"Not authenticated" error**
   - Ensure you're using the correct token format: `Bearer YOUR_TOKEN`
   - Check if your token has expired (30-minute limit)
   - Verify the user account is active

2. **Database connection issues**
   - The SQLite database file will be created automatically
   - Ensure write permissions in the project directory

3. **Email already exists error**
   - Student emails must be unique
   - Use a different email address or update the existing student

4. **CORS errors**
   - Frontend must be running on `http://localhost:3000`
   - Check browser console for specific CORS error messages

### Support

For issues and questions, please create an issue in the repository or contact the development team.