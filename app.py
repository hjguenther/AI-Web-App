from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import gensim.downloader as api

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load a smaller pretrained model (faster to test than full GoogleNews)
model = api.load("word2vec-google-news-300")
#model = api.load("glove-wiki-gigaword-100")

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

    return templates.TemplateResponse(
        "index5.html",
        {"request": request, "message": f"✅ Word cloud for '{word}':", "word": word, "results": results}
    )
