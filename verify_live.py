import urllib.request
import json
import time
import sys

BASE_URL = "http://127.0.0.1:5001"

def run_request(method, url, data=None, headers=None):
    if headers is None:
        headers = {}
    
    if data:
        data = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'

    req = urllib.request.Request(f"{BASE_URL}{url}", data=data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.status
            resp_data = response.read().decode('utf-8')
            return status, json.loads(resp_data)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        print(f"Request failed: {e}")
        return 0, None

def test_live():
    print("Waiting for server to start...")
    time.sleep(2) # Give server time to start

    # 1. Login
    print("Testing Login...")
    status, body = run_request("POST", "/login", {"username": "admin", "password": "password"})
    if status != 200:
        print(f"Login failed: {status} {body}")
        sys.exit(1)
    token = body.get('token')
    print("Login successful, token received.")

    headers = {'x-access-token': token}

    # 2. Create Patient
    print("Testing Create Patient...")
    patient_data = {
        "first_name": "Live",
        "last_name": "Test",
        "phone": "555-0199",
        "gender": "Male",
        "date_of_birth": "1980-01-01"
    }
    status, body = run_request("POST", "/patients", patient_data, headers)
    if status != 201:
        print(f"Create Patient failed: {status} {body}")
        sys.exit(1)
    print("Create Patient successful.")

    # 3. Get Patients
    print("Testing Get Patients...")
    status, body = run_request("GET", "/patients", None, headers)
    if status != 200:
        print(f"Get Patients failed: {status} {body}")
        sys.exit(1)
    
    # Verify our patient is there
    found = False
    patient_id = None
    for p in body:
        if p.get('first_name') == 'Live' and p.get('last_name') == 'Test':
            found = True
            patient_id = p.get('patient_id')
            break
    
    if found:
        print(f"Patient found with ID: {patient_id}")
    else:
        print("Patient not found in list!")
        sys.exit(1)

    # 4. Delete Patient
    print(f"Testing Delete Patient ID {patient_id}...")
    status, body = run_request("DELETE", f"/patients/{patient_id}", None, headers)
    if status != 200:
        print(f"Delete Patient failed: {status} {body}")
        sys.exit(1)
    print("Delete Patient successful.")

    print("\nALL LIVE TESTS PASSED")

if __name__ == "__main__":
    test_live()
