from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .crud import get_items, create_item

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok"}

# HTML homepage
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    items = get_items(db)
    return templates.TemplateResponse("index6.html", {"request": request, "items": items})

# Add item via form
@app.post("/add", response_class=HTMLResponse)
def add_item(name: str = Form(...), db: Session = Depends(get_db)):
    create_item(db, name)
    return RedirectResponse("/", status_code=303)

