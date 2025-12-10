# Skin Clinic API

Final Project for CSE1 - A CRUD REST API with MySQL, Testing, and XML/JSON Output.

## Project Overview

This API allows users to manage patient records for a Skin Clinic. It provides endpoints to Create, Read, Update, and Delete patients. The API is built with Flask and MySQL, secured with JWT authentication, and supports response formatting in both JSON and XML.

## Features

- **CRUD Operations**: Full management of patient records.
- **Search**: Search patients by first or last name.
- **Validation**: Input validation for required fields.
- **Security**: JWT-based authentication for all endpoints.
- **Formatting**: Supports `json` (default) and `xml` output via the `?format=` query parameter.
- **Testing**: Comprehensive unit tests covering all operations.

## Installation

### Prerequisites

- Python 3.x
- MySQL Server

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd skin-clinic-api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database:**
   - Create a MySQL database named `skin_clinic`.
   - Update `config.py` with your database credentials.
   - Import the initial schema (if provided) or ensure the `patients` table exists with the following columns:
     - `patient_id` (INT, PK, Auto Increment)
     - `first_name` (VARCHAR)
     - `last_name` (VARCHAR)
     - `phone` (VARCHAR)
     - `date_of_birth` (DATE)
     - `gender` (ENUM)
     - `email` (VARCHAR)
     - `address` (TEXT)

## Usage

### Running the Application

```bash
flask run
```

### API Endpoints

**Authentication**
- `POST /login`: Get an access token.
  - Body: `{"username": "admin", "password": "password"}` (Default credentials)

**Patients**
*All patient endpoints require `x-access-token` header.*

- `GET /patients`: List all patients.
  - Query Param: `?format=xml` for XML output.
- `GET /patients/<id>`: Get a specific patient.
- `GET /patients/search`: Search patients.
  - Query Param: `?name=<query>`
- `POST /patients`: Create a new patient.
  - Body: `{"first_name": "John", "last_name": "Doe", "phone": "1234567890", ...}`
- `PUT /patients/<id>`: Update a patient.
- `DELETE /patients/<id>`: Delete a patient.

## Testing

Run the automated tests:

```bash
python -m unittest discover -s tests
```
