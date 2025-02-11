from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
import json
from . import models, schemas, crud, dependencies, user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])

@app.post("/create-file/", response_model=schemas.CodeFile)
async def create_code_file(file_data: schemas.CodeFileCreate, db: Session = Depends(dependencies.get_db)):
    # Create a new code file for the user
    db_file = crud.create_code_file(db=db, user_id=1, file_data=file_data)  # user_id = 1 for now
    return db_file

@app.put("/update-file/{file_id}", response_model=schemas.CodeFile)
async def update_code_file(file_id: int, file_data: schemas.CodeFileCreate, db: Session = Depends(dependencies.get_db)):
    # Update the content of an existing code file
    db_file = crud.update_code_file_content(db=db, file_id=file_id, content=file_data.content)
    if db_file:
        return db_file
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.websocket("/ws/{file_id}")
async def websocket_endpoint(websocket: WebSocket, file_id: int, db: Session = Depends(dependencies.get_db)):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        code_data = json.loads(data)
        
        # Locking the code section being edited
        user_id = code_data["user_id"]
        line_number = code_data["line_number"]
        crud.lock_code_section(file_id, user_id, line_number, db)

        # Handle code updates and send back AI suggestions
        file = crud.get_code_file(db, file_id)
        if file:
            ai_suggestions = get_ai_suggestions(file.content)
            await websocket.send_text(f"AI Suggestions: {ai_suggestions}")
        
        # Respond to other users
        await websocket.send_text(f"User {user_id} is editing line {line_number}")
