from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)
title_name="It'ts Movie"

def get_movie_list():
    url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDE5YjliY2E4YjlhY2NjZmY5ODU2NmEzZjc2MDFjZiIsIm5iZiI6MTU2MjUxMjI4Mi44MzM5OTk5LCJzdWIiOiI1ZDIyMGI5YWY0OTVlZTFkOGUzNmI1ZmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.VtGJ0l0NGePgt9s-RBM6c5Ue02NQCatQP5Lh79thDUc"
    }
    response = requests.get(url, headers=headers)

    return response.json() if response.status_code == 200 else {"results": []}

def get_play_now():
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDE5YjliY2E4YjlhY2NjZmY5ODU2NmEzZjc2MDFjZiIsIm5iZiI6MTU2MjUxMjI4Mi44MzM5OTk5LCJzdWIiOiI1ZDIyMGI5YWY0OTVlZTFkOGUzNmI1ZmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.VtGJ0l0NGePgt9s-RBM6c5Ue02NQCatQP5Lh79thDUc"
    }
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {"results": []}

def get_popular():
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDE5YjliY2E4YjlhY2NjZmY5ODU2NmEzZjc2MDFjZiIsIm5iZiI6MTU2MjUxMjI4Mi44MzM5OTk5LCJzdWIiOiI1ZDIyMGI5YWY0OTVlZTFkOGUzNmI1ZmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.VtGJ0l0NGePgt9s-RBM6c5Ue02NQCatQP5Lh79thDUc"
    }

    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {"results": []}

def get_details(id):
    url = "https://api.themoviedb.org/3/movie/{id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDE5YjliY2E4YjlhY2NjZmY5ODU2NmEzZjc2MDFjZiIsIm5iZiI6MTU2MjUxMjI4Mi44MzM5OTk5LCJzdWIiOiI1ZDIyMGI5YWY0OTVlZTFkOGUzNmI1ZmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.VtGJ0l0NGePgt9s-RBM6c5Ue02NQCatQP5Lh79thDUc"
    }

    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {"results": []}


def get_genre(id):
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDE5YjliY2E4YjlhY2NjZmY5ODU2NmEzZjc2MDFjZiIsIm5iZiI6MTU2MjUxMjI4Mi44MzM5OTk5LCJzdWIiOiI1ZDIyMGI5YWY0OTVlZTFkOGUzNmI1ZmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.VtGJ0l0NGePgt9s-RBM6c5Ue02NQCatQP5Lh79thDUc"
    }

    response = requests.get(url, headers=headers)
    
@app.route("/")
def home():
    return render_template('home.html', title=title_name, data=get_movie_list())

@app.route("/now")
def now():
    return render_template('now_playing.html', title=title_name, data=get_play_now())

@app.route("/popular")
def popular():
    return render_template('popular.html', title=title_name, data=get_popular())

@app.route("/detail")
def detail():
    return render_template('detail.html', title=title_name, data=get_details())

