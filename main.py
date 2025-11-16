from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)
title_name="It'ts Movie"

@app.route("/")
def home():

    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDE5YjliY2E4YjlhY2NjZmY5ODU2NmEzZjc2MDFjZiIsIm5iZiI6MTU2MjUxMjI4Mi44MzM5OTk5LCJzdWIiOiI1ZDIyMGI5YWY0OTVlZTFkOGUzNmI1ZmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.VtGJ0l0NGePgt9s-RBM6c5Ue02NQCatQP5Lh79thDUc"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        data = {"results": []}
    print(data)
    return render_template('home.html', title=title_name, data=data)

@app.route("/now")
def now():
    return render_template('now_playing.html', title=title_name)

@app.route("/popular")
def popular():
    return render_template('popular.html', title=title_name)

@app.route("/detail")
def detail():
    return render_template('detail.html', title=title_name)

