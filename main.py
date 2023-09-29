import uvicorn
from dotenv import load_dotenv
import os

from fastapi import Depends, FastAPI
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Column, String, create_engine

app = FastAPI()
BaseModel = declarative_base()


load_dotenv()
def get_db_name():
    name: str = "testdb"
    host: str = "localhost"
    port: int = 5433 # У вас буде 5432
    username: str = "postgres"
    password: str = os.getenv("password")
    return f"postgresql://{username}:{password}@{host}:{port}/{name}"

engine = create_engine(get_db_name())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


class Film(BaseModel):
    __tablename__ = "films"
    film = Column(String, primary_key=True)

@app.post("/add_film")
def add_film(film_name: str, db: Session = Depends(get_db)):

    data: dict = {
        "film": film_name
    }
    payload = Film(**data)
    db.add(payload)
    db.commit()

if __name__ == "__main__":
    uvicorn.run("main:app",
                reload=True,
                host="127.0.0.1",
                port=8000)
