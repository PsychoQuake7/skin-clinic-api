# tests/test_api.py
import unittest
from app import app, SECRET_KEY
import jwt
from datetime import datetime, timedelta

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Create a valid token for testing
        self.token = jwt.encode(
            {'user': 'admin', 'exp': datetime.utcnow() + timedelta(hours=1)},
            SECRET_KEY, algorithm="HS256"
        )

    def test_get_patients_json(self):
        response = self.client.get('/patients', headers={'x-access-token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)

    def test_get_patients_xml(self):
        response = self.client.get('/patients?format=xml', headers={'x-access-token': self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response.content_type)

    def test_create_patient_missing_data(self):
        # Missing required field 'phone'
        response = self.client.post('/patients', json={'first_name':'Test', 'last_name':'User'}, headers={'x-access-token': self.token})
        self.assertEqual(response.status_code, 400)

    def test_create_patient_success(self):
        payload = {
            'first_name': 'Test',
            'last_name': 'Patient',
            'phone': '1234567890',
            'gender': 'Male',
            'date_of_birth': '1990-01-01'
        }
        response = self.client.post('/patients', json=payload, headers={'x-access-token': self.token})
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_access(self):
        response = self.client.get('/patients')  # no token
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
