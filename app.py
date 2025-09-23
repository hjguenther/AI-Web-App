from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import gensim.downloader as api

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load pretrained Google Word2Vec model (small version to avoid heavy downloads)
# For full model, use: model = api.load("word2vec-google-news-300")
model = api.load("glove-wiki-gigaword-100")  # smaller but works the same

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index5.html",
        {"request": request, "message": "Type a word to find similar words 🔤"}
    )

@app.post("/predict", response_class=HTMLResponse)
def predict(request: Request, word: str = Form(...)):
    if word not in model.key_to_index:
        return templates.TemplateResponse(
            "index5.html",
            {"request": request, "message": f"❌ The word '{word}' is not in the vocabulary."}
        )

    # Find top 5 most similar words
    similar_words = model.most_similar(word, topn=5)
    result_list = [f"{w} ({round(score, 3)})" for w, score in similar_words]

    return templates.TemplateResponse(
        "index5.html",
        {"request": request, "message": f"✅ Similar words to '{word}':<br>" + '<br>'.join(result_list)}
    )
