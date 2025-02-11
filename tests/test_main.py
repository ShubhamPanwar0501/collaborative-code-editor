import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models, crud
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db

# Setup for test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def client():
    client = TestClient(app)
    return client

# Test creating a code file
def test_create_code_file(client, db):
    file_data = {
        "filename": "test_file.py",
        "content": "print('Test file')"
    }
    
    response = client.post("/create-file/", json=file_data)
    assert response.status_code == 200
    assert response.json()["filename"] == "test_file.py"
    assert response.json()["content"] == "print('Test file')"

    # Check in the database if the file was created
    db_file = db.query(models.CodeFile).filter(models.CodeFile.filename == "test_file.py").first()
    assert db_file is not None
    assert db_file.filename == "test_file.py"
    assert db_file.content == "print('Test file')"

# Test updating a code file
def test_update_code_file(client, db):
    # First, create a file
    file_data = {
        "filename": "update_test_file.py",
        "content": "print('Old content')"
    }
    response = client.post("/create-file/", json=file_data)
    file_id = response.json()["id"]

    # Update file content
    updated_data = {
        "filename": "update_test_file.py",
        "content": "print('Updated content')"
    }

    response = client.put(f"/update-file/{file_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["content"] == "print('Updated content')"

    # Check in database if the content was updated
    db_file = db.query(models.CodeFile).filter(models.CodeFile.id == file_id).first()
    assert db_file is not None
    assert db_file.content == "print('Updated content')"

# Test WebSocket connection and real-time collaboration
def test_websocket(client, db):
    # Create a file first to associate with the WebSocket
    file_data = {
        "filename": "real_time_test.py",
        "content": "print('Initial content')"
    }
    response = client.post("/create-file/", json=file_data)
    file_id = response.json()["id"]

    # Test WebSocket connection
    with client.websocket_connect(f"/ws/{file_id}") as websocket:
        # Send data simulating a user editing a line
        data = {
            "user_id": 1,
            "line_number": 5,
            "content": "print('Real-time edit')"
        }
        websocket.send_text(str(data))
        
        # Test receiving AI suggestions and user edits in real-time
        response = websocket.receive_text()
        assert "AI Suggestions" in response
        assert f"User 1 is editing line {data['line_number']}" in response

        # Simulate another user editing
        data = {
            "user_id": 2,
            "line_number": 6,
            "content": "print('Another edit')"
        }
        websocket.send_text(str(data))

        # Test receiving AI suggestions and user edits for the second user
        response = websocket.receive_text()
        assert "AI Suggestions" in response
        assert f"User 2 is editing line {data['line_number']}" in response
