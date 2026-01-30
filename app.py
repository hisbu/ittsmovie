from flask import Flask, render_template, jsonify, request, url_for
import requests

app = Flask(__name__)
title_name="It'ts Movies"
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
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"results": [], "error": f"API returned status {response.status_code}"}
    except requests.RequestException as e:
        return {"results": [], "error": f"Could not load data: {str(e)}"}

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
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"results": [], "error": f"API returned status {response.status_code}"}
    except requests.RequestException as e:
        return {"results": [], "error": f"Could not load data: {str(e)}"}

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

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"results": [], "error": f"API returned status {response.status_code}"}
    except requests.RequestException as e:
        return {"results": [], "error": f"Could not load data: {str(e)}"}

def get_trending(page=1, time_window="week"):
    url = f"https://api.themoviedb.org/3/trending/movie/{time_window}"
    params = {
        "language": "en-US",
        "page": page
    }
    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"results": [], "error": f"API returned status {response.status_code}"}
    except requests.RequestException as e:
        return {"results": [], "error": f"Could not load data: {str(e)}"}
    
def get_details(id):
    """
    Ambil detail film dari TMDB, beserta credits, images, dan videos
    supaya template detail punya data yang lengkap.
    """
    url = f"https://api.themoviedb.org/3/movie/{id}"

    params = {
        "language": "en-US",
        "append_to_response": "credits,images,videos",
        "include_image_language": "en,null"
    }

    headers = {
        "accept": "application/json",
        "Authorization": API_KEY
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"results": [], "error": f"API returned status {response.status_code}"}
    except requests.RequestException as e:
        return {"results": [], "error": f"Could not load data: {str(e)}"}


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
    data = get_movie_list(page, sort_by, order)
    error_message = data.get("error")

    return render_template('home.html', 
                           title=title_name, 
                           data=data, 
                           page=data.get("page", 1),
                           total_pages=data.get("total_pages", 1),
                           sort_by=sort_by,
                           error_message=error_message)

@app.route("/index")
def index():
    # Baca time_window dari query parameter, default ke "week"
    time_window = request.args.get('time_window', 'week')
    if time_window not in ['day', 'week']:
        time_window = 'week'
    
    # slider utama: now playing (maks 12 item)
    now_data = get_play_now(page=1)
    now_playing = (now_data or {}).get("results", [])[:12]

    # trending movies (maks 12 item) - sesuai dengan time_window
    trending_data = get_trending(page=1, time_window=time_window)
    trending_movies = (trending_data or {}).get("results", [])[:12]

    # tetap kirim variabel umum agar template aman
    error_message = now_data.get("error") if isinstance(now_data, dict) else None

    return render_template(
        "index.html",
        title=title_name,
        now_playing=now_playing,
        error_message=error_message,
        page=1,
        total_pages=1,
        sort_by="popularity.desc",
        trending_movies=trending_movies,
        time_window=time_window
    )

@app.route("/now")
def now():
    page = int(request.args.get("page", 1))
    data = get_play_now(page)
    error_message = data.get("error")

    return render_template('now_playing.html', 
                            title=title_name, 
                            data=data,
                            total_pages=data.get("total_pages", 1),
                            page=data.get("page", page),
                            error_message=error_message
                            )

@app.route("/popular")
def popular():
    page = int(request.args.get("page", 1))
    data = get_popular(page)
    error_message = data.get("error")
    return render_template('popular.html', 
                            title=title_name, 
                            data=data,
                            total_pages=data.get("total_pages", 1),
                            page=data.get("page", page),
                            error_message=error_message
                            )

@app.route("/api/trending")
def api_trending():
    """API endpoint untuk mendapatkan trending movies dengan filter time_window"""
    time_window = request.args.get('time_window', 'week')
    page = int(request.args.get('page', 1))
    
    # Validasi time_window
    if time_window not in ['day', 'week']:
        time_window = 'week'
    
    data = get_trending(page=page, time_window=time_window)
    trending_movies = (data or {}).get("results", [])[:12]
    
    return jsonify({
        "results": trending_movies,
        "time_window": time_window,
        "error": data.get("error") if isinstance(data, dict) else None
    })

@app.route("/detail")
def detail():
    # try to get id from query string if provided
    movie_id = request.args.get('id')
    data = get_details(movie_id) if movie_id else {"results": [], "error": "No id provided"}
    error_message = data.get("error")
    # build a context-aware back url based on 'src' query param or referrer
    src = request.args.get('src')
    src_page = request.args.get('page')
    src_sort = request.args.get('sort_by')

    if src == 'home':
        back_url = url_for('home', page=src_page or 1, sort_by=src_sort or 'popularity.desc')
    elif src == 'index':
        back_url = url_for('index')
    elif src == 'now':
        back_url = url_for('now', page=src_page or 1)
    elif src == 'popular':
        back_url = url_for('popular', page=src_page or 1)
    else:
        # fallback to referrer or home
        back_url = request.referrer or url_for('home')

    return render_template('detail.html', title=title_name, data=data, error_message=error_message, back_url=back_url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)