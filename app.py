# app.py
from flask import Flask, request, jsonify
import mysql.connector
from config import DB_CONFIG
from utils.helpers import format_response
import jwt
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)

# Secret key for JWT
SECRET_KEY = "supersecretkey"  # in production, store in env variable

# ---------------- Database Connection ----------------
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    return conn

# ---------------- JWT Authentication ----------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(*args, **kwargs)
    return decorated

# Login endpoint to get token
@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Missing username or password'}), 400
    
    # Demo credentials (replace with DB check in production)
    if auth['username'] == 'admin' and auth['password'] == 'password':
        token = jwt.encode(
            {'user': auth['username'], 'exp': datetime.utcnow() + timedelta(hours=1)},
            SECRET_KEY, algorithm="HS256"
        )
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# ---------------- CRUD Endpoints ----------------

# Get all patients
@app.route('/patients', methods=['GET'])
@token_required
def get_all_patients():
    format_type = request.args.get('format', 'json')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return format_response(results, format_type)

# Get a patient by ID
@app.route('/patients/<int:id>', methods=['GET'])
@token_required
def get_patient_by_id(id):
    format_type = request.args.get('format', 'json')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE id=%s", (id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        return jsonify({'message': 'Patient not found'}), 404
    return format_response(result, format_type)

# Search patients by name
@app.route('/patients/search', methods=['GET'])
@token_required
def search_patients_by_name():
    query = request.args.get('name', '')
    format_type = request.args.get('format', 'json')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE name LIKE %s", (f"%{query}%",))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return format_response(results, format_type)

# Create a new patient
@app.route('/patients', methods=['POST'])
@token_required
def create_new_patient():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    if not name or not age:
        return jsonify({'error': 'Missing name or age'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Patient added successfully'}), 201

# Update a patient
@app.route('/patients/<int:id>', methods=['PUT'])
@token_required
def update_patient_record(id):
    data = request.json
    name = data.get('name')
    age = data.get('age')
    if not name or not age:
        return jsonify({'error': 'Missing name or age'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE patients SET name=%s, age=%s WHERE id=%s", (name, age, id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Patient updated successfully'}), 200

# Delete a patient
@app.route('/patients/<int:id>', methods=['DELETE'])
@token_required
def delete_patient_record(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Patient deleted successfully'}), 200

# ---------------- Run Flask App ----------------
if __name__ == "__main__":
    app.run(debug=True)
