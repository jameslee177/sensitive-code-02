from flask import Flask, jsonify, request
import json
import logging

app = Flask(__name__)

# Load user data from an external JSON file
with open('mock_users.json', 'r') as f:
    mock_users = json.load(f)["users"]

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    """
    Logs the user in with email and password.

    ### API Description:
    - **Endpoint**: `/api/login`
    - **Method**: `POST`
    - **Request Body**:
      ```json
      {
        "email": "string",         // User's email address (required)
        "password": "string",      // User's password (required)
        "remember": "boolean"      // Optional flag to remember the session
      }
      ```
    - **Responses**:
      - `200 OK`:
        ```json
        {
          "id": "integer",          // User ID
          "name": "string",         // User's full name
          "email": "string",        // User's email address
          "role": "string"          // User's role (e.g., "admin", "user")
        }
        ```
      - `400 Bad Request`:
        ```json
        {
          "error": "string"         // Error message
        }
        ```

    ### Sensitive Data:
    - The `password` field is validated but excluded from responses.
    """
    input_data = request.json or {}
    email = input_data.get('email')  # sensitive: email address
    password = input_data.get('password')  # sensitive: password

    # Check for missing input
    if not email or not password:
        return jsonify({"error": "Missing input"}), 400

    # Query user from external JSON data
    user = mock_users.get(email)

    # Validate user and password
    if not user or user["password"] != password:  # sensitive: password verification
        return jsonify({"error": "Invalid login credentials"}), 400

    # Simulate session creation
    session = {"user_id": user["id"], "remember": input_data.get("remember", True)}

    # Log the successful login
    logger.info(f"LOGIN OK: User '{email}' logged in successfully. Agent: {request.headers.get('User-Agent')}")

    # Exclude sensitive fields like password from the response
    user_response = {key: value for key, value in user.items() if key != "password"}
    return jsonify(user_response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
