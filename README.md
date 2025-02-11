# Real-Time Collaborative Code Editor with AI-Assisted Debugging

## Project Overview
This project is a **Real-Time Collaborative Code Editor** integrated with **AI-Assisted Debugging**. The platform allows multiple developers to collaborate on code in real-time, providing an environment similar to Google Docs but for coding. The AI component analyzes the code to provide debugging suggestions such as syntax errors, potential bugs, and performance improvements.

This project is built using **FastAPI**, **WebSocket**, **SQLAlchemy**, and includes real-time collaboration capabilities along with AI-based debugging assistance. It is designed for scalability and security, with additional features such as user management, real-time communication, and Docker support.

---

## Core Features

### 1. Real-Time Collaboration
- **Multi-user Editing**: Allow multiple users to edit the same code file simultaneously.
- **Live Sync**: Changes are reflected in real-time using WebSockets.
- **Cursor Tracking**: Real-time tracking of each user’s cursor and active line.

### 2. AI-Assisted Debugging
- **AI Integration**: Integration of an AI model (such as OpenAI Codex or Hugging Face) to analyze the code.
- **Debugging Suggestions**: AI-powered suggestions for syntax errors, potential bugs, and performance improvements.
- **Interactive Feedback**: Users can accept or reject AI suggestions.

### 3. User Management
- **Account Creation**: Users can create accounts and log in to access their code files.
- **Role-based Access Control**: Roles like owner and collaborator for code files.

### 4. Real-Time Communication
- **WebSocket Support**: Real-time updates for code changes using WebSockets.
- **Conflict Resolution**: Handled simultaneous edits using appropriate locking mechanisms.

### 5. Database Integration
- **Database Schema**: SQLAlchemy ORM used for managing users, code files, and sessions in a relational database (PostgreSQL).
- **Persistence**: Code files and editing sessions are stored persistently in the database.

### 6. Security and Authentication
- **JWT Authentication**: Secure endpoints using JWT tokens.
- **Data Encryption**: Sensitive user data is encrypted.
- **Input Validation**: Proper validation to avoid SQL injections and other vulnerabilities.

---

## Technologies Used

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy
- **WebSockets**: For real-time collaboration
- **AI Model**: OpenAI Codex or Hugging Face for AI-assisted debugging
- **Authentication**: JWT tokens for secure user management
- **Real-Time Communication**: WebSockets
- **Caching**: Redis (for caching frequently accessed data)
- **Message Queue**: Redis or RabbitMQ for real-time communication handling
- **Docker**: For containerization and deployment

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ShubhamPanwar0501/collaborative-code-editor.git
cd collaborative-code-editor
```

### 2. Set up a Python Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root of the project with the following variables:
- `DATABASE_URL`: URL for PostgreSQL database (e.g., `postgresql://username:password@localhost/dbname`)
- `REDIS_URL`: URL for Redis caching service (e.g., `redis://localhost:6379/0`)
- `JWT_SECRET_KEY`: Secret key for JWT token encryption.

### 5. Set up the Database
Run migrations to set up the database schema:
```bash
alembic upgrade head
```

### 6. Run the Application
To start the FastAPI application, run:
```bash
uvicorn app.main:app --reload
```
This will start the server on `http://127.0.0.1:8000`.

### 7. Access API Documentation
FastAPI generates interactive documentation for the APIs. You can access it at:
```
http://127.0.0.1:8000/docs
```

---

## Docker Setup

If you prefer using Docker, follow the steps below.

### 1. Build Docker Images
```bash
docker-compose build
```

### 2. Start the Application with Docker
```bash
docker-compose up
```

This will start the FastAPI server and other services like PostgreSQL, Redis, and RabbitMQ, if necessary, for real-time collaboration.

---

## API Endpoints

### 1. `POST /create-file/`
Create a new code file for collaboration.

#### Request:
```json
{
  "filename": "example.py",
  "content": "print('Hello World!')"
}
```

#### Response:
```json
{
  "id": 1,
  "filename": "example.py",
  "content": "print('Hello World!')"
}
```

### 2. `PUT /update-file/{file_id}`
Update the content of an existing code file.

#### Request:
```json
{
  "content": "print('Updated Hello World!')"
}
```

#### Response:
```json
{
  "id": 1,
  "filename": "example.py",
  "content": "print('Updated Hello World!')"
}
```

### 3. `WebSocket /ws/{file_id}`
Real-time collaboration through WebSocket for editing code.

#### Request:
- Send a JSON object to simulate code editing:
  ```json
  {
    "user_id": 1,
    "line_number": 10
  }
  ```

#### Response:
- The server sends updates about the user’s current action (e.g., editing line 10).

---

## Testing

Unit tests and integration tests are written using `pytest`. To run the tests:

```bash
pytest
```

To run tests for a specific file, use:

```bash
pytest test_main.py
```