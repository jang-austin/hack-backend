# hack-backend

A Flask-based backend application with robust form input validation.

## Features

- Form submission endpoint with comprehensive validation
- Email format validation
- Age range validation (0-150)
- Name length and presence validation
- RESTful API design
- Comprehensive test coverage

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The application will start on `http://localhost:5000`

**Note**: By default, the application runs in production mode (debug=False). To enable debug mode for development, set the `FLASK_DEBUG` environment variable:
```bash
FLASK_DEBUG=true python app.py
```

## API Endpoints

### GET /
Returns information about available endpoints.

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

### POST /submit-form
Submit a form with validation.

**Request body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "age": 30
}
```

**Success Response (200):**
```json
{
  "message": "Form submitted successfully",
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30
  }
}
```

**Error Response (400):**
```json
{
  "errors": {
    "email": "Invalid email format",
    "age": "Age must be between 0 and 150"
  }
}
```

## Validation Rules

- **Email**: Must be a valid email format (e.g., user@example.com)
- **Age**: Must be a number between 0 and 150
- **Name**: Must be 2-100 characters long and not empty

## Running Tests

Run the test suite with pytest:
```bash
pytest test_app.py -v
```

## Development

The application uses Flask for the web framework and includes:
- Input validation for form fields
- Error handling with appropriate status codes
- JSON API responses
- Unit tests with pytest
