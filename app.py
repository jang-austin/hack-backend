"""
Flask backend application with form input validation
"""
from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)


def validate_email(email):
    """Validate email format"""
    if not email:
        return False, "Email is required"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, "Valid"


def validate_age(age):
    """Validate age field"""
    if age is None:
        return False, "Age is required"
    
    try:
        age_int = int(age)
        if age_int < 0 or age_int > 150:
            return False, "Age must be between 0 and 150"
    except (ValueError, TypeError):
        return False, "Age must be a valid number"
    
    return True, "Valid"


def validate_name(name):
    """Validate name field"""
    if not name or not name.strip():
        return False, "Name is required"
    
    name_stripped = name.strip()
    
    if len(name_stripped) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name_stripped) > 100:
        return False, "Name must be 100 characters or less"
    
    return True, "Valid"


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'message': 'Welcome to the form validation API',
        'endpoints': {
            '/submit-form': 'POST - Submit a form with validation',
            '/health': 'GET - Health check endpoint'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


@app.route('/submit-form', methods=['POST'])
def submit_form():
    """Handle form submission with validation"""
    data = request.get_json()
    
    if data is None:
        return jsonify({'error': 'No data provided'}), 400
    
    errors = {}
    
    # Validate email
    email = data.get('email')
    email_valid, email_msg = validate_email(email)
    if not email_valid:
        errors['email'] = email_msg
    
    # Validate age
    age = data.get('age')
    age_valid, age_msg = validate_age(age)
    if not age_valid:
        errors['age'] = age_msg
    
    # Validate name
    name = data.get('name')
    name_valid, name_msg = validate_name(name)
    if not name_valid:
        errors['name'] = name_msg
    
    # Return errors if validation failed
    if errors:
        return jsonify({'errors': errors}), 400
    
    # If validation passed, return success
    return jsonify({
        'message': 'Form submitted successfully',
        'data': {
            'name': name,
            'email': email,
            'age': age
        }
    }), 200


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
