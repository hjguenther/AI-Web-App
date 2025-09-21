from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Tell FastAPI where templates are
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    # Must pass {"request": request}, or it hangs
    return templates.TemplateResponse(
        "index2.html",
        {"request": request, "message": "This will be replaced with some fancy AI magic"}
    )
