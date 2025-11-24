from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
title_name="It'ts Movie"
pages_button = 0
pages = 1 + pages_button
API_KEY = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDE5YjliY2E4YjlhY2NjZmY5ODU2NmEzZjc2MDFjZiIsIm5iZiI6MTU2MjUxMjI4Mi44MzM5OTk5LCJzdWIiOiI1ZDIyMGI5YWY0OTVlZTFkOGUzNmI1ZmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.VtGJ0l0NGePgt9s-RBM6c5Ue02NQCatQP5Lh79thDUc"

def get_movie_list(page=1, sort_by="popularity.desc", order="desc"):
    url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "sort_by": sort_by,
        "page": page
    }

    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }
    response = requests.get(url, headers=headers, params=params)

    return response.json() if response.status_code == 200 else {"results": []}

def get_play_now(page=1):
    url = "https://api.themoviedb.org/3/movie/now_playing"
    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": page
    }

    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else {"results": []}

def get_popular(page=1):
    url = "https://api.themoviedb.org/3/movie/popular"
    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": page
    }
    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }

    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else {"results": []}

def get_details(id):
    url = "https://api.themoviedb.org/3/movie/{id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }

    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {"results": []}


def get_genre(id):
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en"
    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }

    response = requests.get(url, headers=headers)
    
@app.route("/")
def home():
    page = int(request.args.get("page", 1))
    sort_by = request.args.get("sort_by", "popularity.desc")
    order = request.args.get("order")
    data = get_movie_list(page)

    return render_template('home.html', 
                           title=title_name, 
                           data=get_movie_list(page, sort_by, order), 
                           page=data["page"],
                           total_pages=data["total_pages"],
                           sort_by=sort_by)


@app.route("/now")
def now():
    page = int(request.args.get("page", 1))
    data = get_play_now(page)

    return render_template('now_playing.html', 
                            title=title_name, 
                            data=get_play_now(page),
                            total_pages=data["total_pages"],
                            page=data["page"]
                            )

@app.route("/popular")
def popular():
    page = int(request.args.get("page", 1))
    data = get_popular(page)
    return render_template('popular.html', 
                            title=title_name, 
                            data=get_popular(page),
                            total_pages=data["total_pages"],
                            page=data["page"]
                            )

@app.route("/detail")
def detail():
    return render_template('detail.html', title=title_name, data=get_details())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004, debug=True)