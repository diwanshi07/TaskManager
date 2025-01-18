# Task Manager

Task Manager is a web application that allows users to manage tasks, with features like task creation, editing, deletion, and user authentication. It supports JWT-based authentication and uses a RESTful API.

## Features

- User registration and login using JWT tokens.
- Task creation, reading, updating, and deletion.
- Pagination and filtering of tasks.
- Secure authentication using JSON Web Tokens (JWT).
- Logging and error handling using custom loggers.

## Technologies Used

- **Backend**: Python, Flask, Flask-RESTX
- **Database**: SQLite (configured through SQLAlchemy)
- **Authentication**: JWT (JSON Web Tokens)
- **Security**: Password hashing using `werkzeug.security`
- **Logging**: Custom logging with `logging` and integration with Loki (optional)
- **Environment**: Python 3.x
- **Additional Libraries**: `Flask-JWT-Extended`, `Flask-SQLAlchemy`, `werkzeug`, `dotenv`, `requests`

## Setup Instructions

Follow these steps to get the project up and running on your local machine.

### Prerequisites

- Python 3.x
- pip (Python package installer)
- A `.env` file for environment variables

### Clone the Repository

```bash
git clone https://github.com/yourusername/task-manager.git
cd task-manager
Create a Virtual Environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Set Up Environment Variables
Create a .env file in the root directory of your project with the following variables:

bash
Copy
Edit
SECRET_KEY=your-secret-key
JWT_EXPIRATION_TIME=1  # Expiration time for JWT in hours
LOKI_HOST=your-loki-server-url (if using Loki for logging)
Run the Application
bash
Copy
Edit
python app.py
The application will run on http://127.0.0.1:8009.

API Endpoints
User Management
POST /api/v1/users/signup: Create a new user.
POST /api/v1/users/login: Log in and get a JWT token.
Task Management
GET /api/v1/tasks/: Fetch all tasks for the logged-in user with pagination.
POST /api/v1/tasks/: Create a new task for the logged-in user.
GET /api/v1/tasks/<task_id>: Fetch a specific task for the logged-in user.
PUT /api/v1/tasks/<task_id>: Update a task for the logged-in user.
DELETE /api/v1/tasks/<task_id>: Delete a specific task.
DELETE /api/v1/tasks/delete_all: Delete all tasks for the logged-in user.
Logs
Logs can be seen in the console or configured to be sent to a Loki server if you are using it for monitoring.

Testing
To run the tests, you can use pytest.

Run Tests
bash
Copy
Edit
pytest
Contributing
Fork the repository.
Create your feature branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a pull request.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Inspired by Flask's official documentation.
Special thanks to the open-source community for contributing to libraries and tools that help speed up development.
```
