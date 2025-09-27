from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, text
import gensim.downloader as api
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load pretrained word2vec model
#model = api.load("word2vec-google-news-300")
model = api.load("glove-wiki-gigaword-100")

# Connect to PostgreSQL using Render-injected DATABASE_URL
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url, connect_args={"sslmode": "require"})

# Create table if it doesn't exist
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS word_predictions (
            id SERIAL PRIMARY KEY,
            input_word TEXT NOT NULL,
            similar_words TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index5.html",
        {"request": request, "message": "Type a word to generate a word cloud 🔤", "word": None, "results": []}
    )

@app.post("/predict", response_class=HTMLResponse)
def predict(request: Request, word: str = Form(...)):
    word = word.lower().strip()

    if word not in model.key_to_index:
        return templates.TemplateResponse(
            "index5.html",
            {"request": request, "message": f"❌ The word '{word}' is not in the vocabulary.", "word": None, "results": []}
        )

    # Find top 8 most similar words
    similar_words = model.most_similar(word, topn=8)
    results = [{"text": w, "weight": score} for w, score in similar_words]

    # Format similar words for DB storage
    similar_text = ", ".join([f"{w}:{round(score, 3)}" for w, score in similar_words])

    # Insert into database
    with engine.connect() as conn:
        conn.execute(
            text("INSERT INTO word_predictions (input_word, similar_words) VALUES (:word, :similar)"),
            {"word": word, "similar": similar_text}
        )

    return templates.TemplateResponse(
        "index5.html",
        {"request": request, "message": f"✅ Word cloud for '{word}':", "word": word, "results": results}
    )

