from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)
title_name="It'ts Movie"
pages_button = 0
pages = 1 + pages_button
API_KEY = "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZDE5YjliY2E4YjlhY2NjZmY5ODU2NmEzZjc2MDFjZiIsIm5iZiI6MTU2MjUxMjI4Mi44MzM5OTk5LCJzdWIiOiI1ZDIyMGI5YWY0OTVlZTFkOGUzNmI1ZmEiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.VtGJ0l0NGePgt9s-RBM6c5Ue02NQCatQP5Lh79thDUc"

def get_movie_list(page=1, sort="popularity", order="desc"):
    urut = f"{sort}.{order}"
    print(urut)
    # url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
    url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "sort_by": f"{sort}.{order}",
        "page": page
    }

    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }
    response = requests.get(url, headers=headers, params=params)

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
    page = int(request.args.get("page", 1))
    sort = request.args.get("sort", "popularity")
    order = request.args.get("order", "desc")
    data = get_movie_list(page)

    return render_template('home.html', 
                           title=title_name, 
                           data=get_movie_list(page, sort, order), 
                           page=data["page"],
                           total_pages=data["total_pages"],
                           sort=sort,
                           order=order)

    # page = int(request.args.get("page", 1))   # <-- ini yang benar

    # data = get_movie_list(page)

    # return render_template(
    #     'home.html',
    #     title=title_name,
    #     data=data["results"],   # jangan panggil get_movie_list() lagi
    #     page=data["page"],
    #     total_pages=data["total_pages"]
    # )

@app.route("/now")
def now():
    return render_template('now_playing.html', title=title_name, data=get_play_now())

@app.route("/popular")
def popular():
    return render_template('popular.html', title=title_name, data=get_popular())

@app.route("/detail")
def detail():
    return render_template('detail.html', title=title_name, data=get_details())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004, debug=True)