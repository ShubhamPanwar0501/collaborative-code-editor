from sqlalchemy.orm import Session
from app import models, schemas
import redis

# Redis client setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_code_file(db: Session, file_id: int):
    return db.query(models.CodeFile).filter(models.CodeFile.id == file_id).first()

def lock_code_section(file_id: int, user_id: int, line: int, db: Session):
    """Lock a specific section of code for editing."""
    redis_client.set(f"lock:{file_id}:{line}", user_id, ex=60)  # Lock for 60 seconds
    

# Function to create a new code file
def create_code_file(db: Session, user_id: int, file_data: schemas.CodeFileCreate):
    db_code_file = models.CodeFile(**file_data.dict(), user_id=user_id)
    db.add(db_code_file)
    db.commit()
    db.refresh(db_code_file)
    return db_code_file

# Function to update an existing code file's content
def update_code_file_content(db: Session, file_id: int, content: str):
    db_code_file = db.query(models.CodeFile).filter(models.CodeFile.id == file_id).first()
    if db_code_file:
        db_code_file.content = content
        db.commit()
        db.refresh(db_code_file)
    return db_code_file
