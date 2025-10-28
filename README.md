# AI-Web-App
This repo walk through the different attempts at making an AI web app. The different branches of playfully show different aspects of creating a web app from python. First the main branch and "AI-Magic" branch are a basic landing page to test the repo can be hosted with Render's free services. The website could be found here: https://ai-web-app-s62g.onrender.com/. The Database repo is a different app design, it's a text box that inserts the string as a new entry to the database and displays the table in the UI. The "Llama-API" branch is a different app that displays a textbox to chat and query the Tiny LLama API. The "Word-Cloud" branch displays a wordcloud of text that is most similar to the word typed in and queries the word2vec-google-news300 LLM via API.

Why the different app designs across repos? This was an experiement to see how to host an LLM web app, thus the hosting and the LLM api calls were the learnings.

The different iterations of web app creation were tested locally and via the Render web services. One learning is that render's free services did not have enough resources to host the API calling apps, yet it was successful for the landing page and the database page. One main take away from this experience is the huggingface spaces are very robust ways to test different LLMs in a web app interface. We ended up using this interface moving forward. This website can be found here: https://huggingface.co/spaces/MiaHeidiJordan/Taisty

This is a project for the Rocky Mountain AI Women's Code Lab.
