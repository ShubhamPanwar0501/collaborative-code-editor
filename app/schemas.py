from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True

class CodeFileBase(BaseModel):
    filename: str
    content: str

class CodeFileCreate(CodeFileBase):
    pass

class CodeFile(CodeFileBase):
    id: int

    class Config:
        orm_mode = True
