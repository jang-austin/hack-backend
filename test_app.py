"""
Unit tests for form validation
"""
import pytest
import json
from app import app, validate_email, validate_age, validate_name


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestValidationFunctions:
    """Test individual validation functions"""
    
    def test_validate_email_valid(self):
        """Test valid email addresses"""
        assert validate_email('test@example.com')[0] is True
        assert validate_email('user.name@example.co.uk')[0] is True
        assert validate_email('user+tag@domain.com')[0] is True
    
    def test_validate_email_invalid(self):
        """Test invalid email addresses"""
        assert validate_email('')[0] is False
        assert validate_email('invalid')[0] is False
        assert validate_email('invalid@')[0] is False
        assert validate_email('@example.com')[0] is False
        assert validate_email('test@.com')[0] is False
    
    def test_validate_age_valid(self):
        """Test valid ages"""
        assert validate_age(25)[0] is True
        assert validate_age(0)[0] is True
        assert validate_age(150)[0] is True
        assert validate_age('30')[0] is True
    
    def test_validate_age_invalid(self):
        """Test invalid ages"""
        assert validate_age(None)[0] is False
        assert validate_age(-1)[0] is False
        assert validate_age(151)[0] is False
        assert validate_age('abc')[0] is False
        assert validate_age('')[0] is False
    
    def test_validate_name_valid(self):
        """Test valid names"""
        assert validate_name('John')[0] is True
        assert validate_name('Jane Doe')[0] is True
        assert validate_name('A' * 100)[0] is True
        assert validate_name('  John  ')[0] is True  # Whitespace should be trimmed
    
    def test_validate_name_invalid(self):
        """Test invalid names"""
        assert validate_name('')[0] is False
        assert validate_name('   ')[0] is False
        assert validate_name('A')[0] is False
        assert validate_name('A' * 101)[0] is False
        assert validate_name('  ' + 'A' * 101 + '  ')[0] is False  # Over 100 chars after trimming


class TestFormEndpoint:
    """Test the form submission endpoint"""
    
    def test_submit_form_valid(self, client):
        """Test valid form submission"""
        response = client.post('/submit-form',
                              data=json.dumps({
                                  'name': 'John Doe',
                                  'email': 'john@example.com',
                                  'age': 30
                              }),
                              content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Form submitted successfully'
        assert data['data']['name'] == 'John Doe'
    
    def test_submit_form_invalid_email(self, client):
        """Test form submission with invalid email"""
        response = client.post('/submit-form',
                              data=json.dumps({
                                  'name': 'John Doe',
                                  'email': 'invalid-email',
                                  'age': 30
                              }),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data
        assert 'email' in data['errors']
    
    def test_submit_form_invalid_age(self, client):
        """Test form submission with invalid age"""
        response = client.post('/submit-form',
                              data=json.dumps({
                                  'name': 'John Doe',
                                  'email': 'john@example.com',
                                  'age': -5
                              }),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data
        assert 'age' in data['errors']
    
    def test_submit_form_invalid_name(self, client):
        """Test form submission with invalid name"""
        response = client.post('/submit-form',
                              data=json.dumps({
                                  'name': '',
                                  'email': 'john@example.com',
                                  'age': 30
                              }),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data
        assert 'name' in data['errors']
    
    def test_submit_form_multiple_errors(self, client):
        """Test form submission with multiple validation errors"""
        response = client.post('/submit-form',
                              data=json.dumps({
                                  'name': '',
                                  'email': 'invalid',
                                  'age': 200
                              }),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data
        assert 'name' in data['errors']
        assert 'email' in data['errors']
        assert 'age' in data['errors']
    
    def test_submit_form_no_data(self, client):
        """Test form submission with no data"""
        response = client.post('/submit-form',
                              data=json.dumps({}),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'errors' in data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_index_endpoint(self, client):
        """Test index endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'endpoints' in data
