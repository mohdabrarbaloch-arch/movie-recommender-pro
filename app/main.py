import os
from pathlib import Path
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
TMDB_BASE = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

HEADERS = {"Authorization": f"Bearer {TMDB_TOKEN}"}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GENRE_IDS = {
    "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35,
    "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751,
    "Fantasy": 14, "Horror": 27, "Music": 10402, "Mystery": 9648,
    "Romance": 10749, "Sci-Fi": 878, "Thriller": 53, "War": 10752,
    "Western": 37,
}

EPOCH_TITLES = [
    "Silent Era", "Pre-Code", "Golden Age", "Classic Hollywood",
    "New Wave", "Blockbuster Era", "Modern Age"
]

def tmdb_get(endpoint, params=None):
    url = f"{TMDB_BASE}/{endpoint}"
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

def movie_embed(tmdb_id, imdb_id=None):
    primary = f"https://vsembed.ru/embed/movie/{tmdb_id}"
    sources = [
        primary,
        f"https://www.2embed.cc/embed/{tmdb_id}",
        f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1",
    ]
    return primary, sources

def tv_embed(tmdb_id, season, episode):
    primary = f"https://vsembed.ru/embed/tv/{tmdb_id}/{season}/{episode}"
    sources = [
        primary,
        f"https://www.2embed.cc/embed/{tmdb_id}?s={season}&e={episode}",
        f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1&s={season}&e={episode}",
        f"https://vidsrc.to/embed/tv/{tmdb_id}/{season}/{episode}",
    ]
    return primary, sources

def build_movie(m):
    genres = []
    if "genre_ids" in m:
        id_to_name = {v: k for k, v in GENRE_IDS.items()}
        genres = [id_to_name.get(gid) for gid in m.get("genre_ids", []) if id_to_name.get(gid)]
    tid = m["id"]
    primary = f"https://vsembed.ru/embed/movie/{tid}"
    sources = [
        primary,
        f"https://www.2embed.cc/embed/{tid}",
        f"https://multiembed.mov/?video_id={tid}&tmdb=1",
    ]
    item = {
        "id": tid,
        "title": m.get("title", ""),
        "poster": f"{IMG_BASE}{m['poster_path']}" if m.get("poster_path") else None,
        "backdrop": f"{IMG_BASE}{m['backdrop_path']}" if m.get("backdrop_path") else None,
        "year": (m.get("release_date") or "")[:4],
        "rating": round(m.get("vote_average", 0), 1),
        "overview": m.get("overview", ""),
        "media_type": "movie",
        "genres": genres,
        "embed_url": primary,
        "embed_sources": sources,
    }
    return item

def build_tv(t):
    tid = t["id"]
    primary = f"https://vsembed.ru/embed/tv/{tid}/1/1"
    sources = [
        primary,
        f"https://www.2embed.cc/embed/{tid}?s=1&e=1",
        f"https://multiembed.mov/?video_id={tid}&tmdb=1&s=1&e=1",
        f"https://vidsrc.to/embed/tv/{tid}/1/1",
    ]
    item = {
        "id": tid,
        "title": t.get("name", ""),
        "poster": f"{IMG_BASE}{t['poster_path']}" if t.get("poster_path") else None,
        "backdrop": f"{IMG_BASE}{t['backdrop_path']}" if t.get("backdrop_path") else None,
        "year": (t.get("first_air_date") or "")[:4],
        "rating": round(t.get("vote_average", 0), 1),
        "overview": t.get("overview", ""),
        "media_type": "tv",
        "embed_url": primary,
        "embed_sources": sources,
    }
    return item

@app.get("/")
def index():
    return {"message": "MovieBox API - Powered by TMDB"}

@app.get("/search")
def search(q: str = "", limit: int = 10):
    if not q.strip():
        return []
    d = tmdb_get("search/multi", {"query": q, "language": "en-US", "page": 1})
    results = d.get("results", [])[:limit]
    out = []
    for r in results:
        if r.get("media_type") == "movie":
            out.append(build_movie(r))
        elif r.get("media_type") == "tv":
            out.append(build_tv(r))
    return out

@app.get("/trending")
def trending(media_type: str = "movie", limit: int = 20):
    d = tmdb_get(f"trending/{media_type}/week", {"language": "en-US"})
    results = d.get("results", [])[:limit]
    if media_type == "tv":
        return [build_tv(t) for t in results]
    return [build_movie(m) for m in results]

@app.get("/movie/{movie_id}")
def movie_detail(movie_id: int):
    d = tmdb_get(f"movie/{movie_id}", {"language": "en-US"})
    if not d or "title" not in d:
        return {"error": "Movie not found"}
    primary, sources = movie_embed(d["id"], d.get("imdb_id"))
    return {
        "id": d["id"],
        "title": d["title"],
        "poster": f"{IMG_BASE}{d['poster_path']}" if d.get("poster_path") else None,
        "backdrop": f"{IMG_BASE}{d['backdrop_path']}" if d.get("backdrop_path") else None,
        "year": (d.get("release_date") or "")[:4],
        "rating": round(d.get("vote_average", 0), 1),
        "genres": [g["name"] for g in d.get("genres", [])],
        "overview": d.get("overview", ""),
        "runtime": d.get("runtime"),
        "imdb_id": d.get("imdb_id"),
        "embed_url": primary,
        "embed_sources": sources,
        "media_type": "movie",
    }

@app.get("/tv/{tv_id}")
def tv_detail(tv_id: int):
    d = tmdb_get(f"tv/{tv_id}", {"language": "en-US"})
    if not d or "name" not in d:
        return {"error": "TV show not found"}
    seasons = []
    for s in d.get("seasons", []):
        if s["season_number"] > 0:
            seasons.append({
                "season": s["season_number"],
                "episodes": s.get("episode_count", 0),
                "poster": f"{IMG_BASE}{s['poster_path']}" if s.get("poster_path") else None,
            })
    primary, sources = tv_embed(d["id"], 1, 1)
    return {
        "id": d["id"],
        "title": d.get("name", ""),
        "poster": f"{IMG_BASE}{d['poster_path']}" if d.get("poster_path") else None,
        "backdrop": f"{IMG_BASE}{d['backdrop_path']}" if d.get("backdrop_path") else None,
        "year": (d.get("first_air_date") or "")[:4],
        "rating": round(d.get("vote_average", 0), 1),
        "overview": d.get("overview", ""),
        "media_type": "tv",
        "seasons": seasons,
        "embed_url": primary,
        "embed_sources": sources,
    }

@app.get("/tv/{tv_id}/season/{season_num}")
def tv_season(tv_id: int, season_num: int):
    d = tmdb_get(f"tv/{tv_id}/season/{season_num}", {"language": "en-US"})
    if not d or "episodes" not in d:
        return {"error": "Season not found"}
    episodes = []
    for ep in d.get("episodes", []):
        primary, sources = tv_embed(tv_id, season_num, ep["episode_number"])
        episodes.append({
            "id": ep["id"],
            "episode": ep["episode_number"],
            "title": ep["name"],
            "overview": ep.get("overview", ""),
            "still": f"{IMG_BASE}{ep['still_path']}" if ep.get("still_path") else None,
            "rating": round(ep.get("vote_average", 0), 1),
            "embed_url": primary,
            "embed_sources": sources,
        })
    return {"show_id": tv_id, "season": season_num, "episodes": episodes}

@app.get("/genre/{genre_id}")
def by_genre(genre_id: int, page: int = 1):
    d = tmdb_get("discover/movie", {
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "page": page,
        "language": "en-US",
    })
    return [build_movie(m) for m in d.get("results", [])]

@app.get("/recommendations/{media_type}/{content_id}")
def recommendations(media_type: str, content_id: int):
    d = tmdb_get(f"{media_type}/{content_id}/recommendations", {"language": "en-US"})
    results = d.get("results", [])[:12]
    if media_type == "tv":
        return [build_tv(t) for t in results]
    return [build_movie(m) for m in results]

@app.get("/music")
def music(page: int = 1):
    d = tmdb_get("discover/movie", {
        "with_genres": "10402",
        "sort_by": "popularity.desc",
        "page": page,
        "language": "en-US",
    })
    return [build_movie(m) for m in d.get("results", [])]

@app.get("/short-videos")
def short_videos():
    d = tmdb_get("trending/movie/week", {"language": "en-US"})
    items = []
    for m in d.get("results", [])[:10]:
        vids = tmdb_get(f"movie/{m['id']}/videos", {"language": "en-US"})
        trailer = None
        for v in vids.get("results", []):
            if v["type"] == "Trailer" and v["site"] == "YouTube":
                trailer = v["key"]
                break
        if trailer:
            items.append({
                "id": m["id"],
                "title": m["title"],
                "poster": f"{IMG_BASE}{m['poster_path']}" if m.get("poster_path") else None,
                "year": (m.get("release_date") or "")[:4],
                "rating": round(m.get("vote_average", 0), 1),
                "trailer_key": trailer,
                "embed_url": f"https://www.youtube.com/embed/{trailer}?autoplay=1",
            })
    return items

@app.get("/hero-content")
def hero_content(limit: int = 10):
    d = tmdb_get("trending/movie/week", {"language": "en-US"})
    results = d.get("results", [])[:limit]
    items = []
    for m in results:
        items.append({
            "id": m["id"],
            "title": m["title"],
            "poster": f"{IMG_BASE}{m['poster_path']}" if m.get("poster_path") else None,
            "backdrop": f"{IMG_BASE}{m['backdrop_path']}" if m.get("backdrop_path") else None,
            "year": (m.get("release_date") or "")[:4],
            "rating": round(m.get("vote_average", 0), 1),
            "overview": m.get("overview", ""),
        })
    return items

@app.get("/all-movies")
def all_movies(page: int = 1):
    d = tmdb_get("discover/movie", {
        "sort_by": "popularity.desc",
        "page": page,
        "language": "en-US",
    })
    return [build_movie(m) for m in d.get("results", [])]

HOME_GENRES = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Thriller", "Animation"]

@app.get("/home")
def home_page():
    result = {"trending": [], "sections": []}
    d = tmdb_get("trending/movie/week", {"language": "en-US"})
    result["trending"] = [build_movie(m) for m in d.get("results", [])[:10]]
    for g in HOME_GENRES:
        gid = GENRE_IDS.get(g)
        if not gid:
            continue
        d = tmdb_get("discover/movie", {"with_genres": gid, "sort_by": "popularity.desc", "page": 1, "language": "en-US"})
        movies = [build_movie(m) for m in d.get("results", [])[:20]]
        if movies:
            result["sections"].append({"genre": g, "movies": movies})
    return result

FRONTEND_BUILD = None
for p in [Path(__file__).parent.parent / "frontend" / "build",
          Path(os.getcwd()) / "frontend" / "build",
          Path("frontend") / "build"]:
    if (p / "index.html").exists():
        FRONTEND_BUILD = p
        break

if FRONTEND_BUILD:
    app.mount("/static", StaticFiles(directory=str(FRONTEND_BUILD / "static")), name="static")
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        return FileResponse(str(FRONTEND_BUILD / "index.html"))
