import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

TMDB_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
TMDB_BASE = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

HEADERS = {}
if TMDB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {TMDB_TOKEN}"

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

def tmdb_get(endpoint, params=None):
    if not TMDB_TOKEN:
        return {}
    url = f"{TMDB_BASE}/{endpoint}"
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        return r.json() if r.status_code == 200 else {}
    except:
        return {}

# ---- FALLBACK MOVIES (no API key needed) ----
FALLBACK_MOVIES = [
    {"id": 550, "title":"Fight Club","poster_path":"/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg","backdrop_path":"/hZkgoQYus5dXo3H8T7Uef6DNknx.jpg","year":"1999","rating":8.4,"genres":["Drama"],"overview":"A ticking-Loss, disillusioned insurance clerk and a mysterious soap salesman create an underground fight club."},
    {"id": 680, "title":"Pulp Fiction","poster_path":"/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg","backdrop_path":"/suaEOtk1N1sgg2MTM7oZd2cfVp3.jpg","year":"1994","rating":8.5,"genres":["Crime","Drama"],"overview":"The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption."},
    {"id": 238, "title":"The Godfather","poster_path":"/3bhkrj58Vtu7enYsRolD1fZdja1.jpg","backdrop_path":"/tmU7GeKVybMWFButWEGl2M4GeiP.jpg","year":"1972","rating":8.7,"genres":["Drama","Crime"],"overview":"The aging patriarch of an organized crime dynasty transfers control to his reluctant son."},
    {"id": 155, "title":"The Dark Knight","poster_path":"/qJ2tW6WMUDux911BytTEkCq2B08.jpg","backdrop_path":"/nMKdUUepR0i5zn0y1T4CsSB5ez.jpg","year":"2008","rating":8.5,"genres":["Action","Crime","Drama"],"overview":"When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological tests."},
    {"id": 244786, "title":"Whiplash","poster_path":"/7fn624j5lj3xTme2SgiLCeuedmO.jpg","backdrop_path":"/6oCHlhgLxqrCkY21O76bPulL3Tq.jpg","year":"2014","rating":8.4,"genres":["Drama","Music"],"overview":"A promising young drummer enrolls at a music conservatory where an abusive instructor will stop at nothing."},
    {"id": 11, "title":"Star Wars","poster_path":"/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg","backdrop_path":"/zqkmTXzjkAgXmEWLRsY4UpTWCeo.jpg","year":"1977","rating":8.2,"genres":["Action","Adventure","Sci-Fi"],"overview":"Luke Skywalker joins forces with a Jedi Knight to rescue a princess from the Galactic Empire."},
    {"id": 497, "title":"The Green Mile","poster_path":"/velWPhVMQeQKcxggNEU8YmIo52R.jpg","backdrop_path":"/l6hQWH9eDksNJNiXWYRkWqikOdu.jpg","year":"1999","rating":8.5,"genres":["Drama","Crime","Fantasy"],"overview":"A death row inmate with mysterious powers changes the lives of the guards."},
    {"id": 807, "title":"Se7en","poster_path":"/69Sns8WoET6CfaYlIkHbla4l7nC.jpg","backdrop_path":"/zeE2Z3YbKBG5WDCmlVURsFznPkt.jpg","year":"1995","rating":8.3,"genres":["Crime","Drama","Thriller"],"overview":"Two detectives hunt a serial killer who uses the seven deadly sins as his motives."},
    {"id": 278, "title":"The Shawshank Redemption","poster_path":"/9cjIGRQL1m4E87FkTJkzMIo2SU.jpg","backdrop_path":"/9Xp3gwTShH6yP7VqXqE6a4YrO5.jpg","year":"1994","rating":8.7,"genres":["Drama"],"overview":"Over the course of several years, two convicts form a friendship, seeking consolation and eventual redemption."},
    {"id": 27205, "title":"Inception","poster_path":"/oYuLEt3zVCKq57qu2F8dT7NIa6f.jpg","backdrop_path":"/8ZTVqvKDQ8emSGUEMjsS4yHAwrp.jpg","year":"2010","rating":8.4,"genres":["Action","Sci-Fi","Adventure"],"overview":"A thief who steals corporate secrets through dream-sharing technology is given the task of planting an idea."},
    {"id": 769, "title":"GoodFellas","poster_path":"/aKuFiU82s5ISJDx3LhOM0TcarD3.jpg","backdrop_path":"/gEPrVmG4DNvBxgn5uwQm1QFcq9.jpg","year":"1990","rating":8.5,"genres":["Drama","Crime"],"overview":"The story of Henry Hill and his life in the mob, covering his relationship with his wife and his mob partners."},
    {"id": 13, "title":"Forrest Gump","poster_path":"/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg","backdrop_path":"/3h1JZGDhZ8nzxdE7W5oX6kA7C2.jpg","year":"1994","rating":8.5,"genres":["Comedy","Drama","Romance"],"overview":"The presidencies of Kennedy and Johnson through the eyes of an Alabama man with an IQ of 75."},
    {"id": 24, "title":"Kill Bill: Vol. 1","poster_path":"/v7TaX8kXMXs5y3GREP4FHf2TtEP.jpg","backdrop_path":"/mtKbXjYsxkvlG1B7bo5rHkRMk7.jpg","year":"2003","rating":8.2,"genres":["Action","Crime","Thriller"],"overview":"An assassin is shot by her treacherous organization and left for dead. She wakes from a coma to seek revenge."},
    {"id": 393, "title":"Kill Bill: Vol. 2","poster_path":"/2yhg0mMs0wjGp34JXH7v9aXKcbe.jpg","backdrop_path":"/2BLxUPcGAZSBbrQrvfF6kqZFGxQ.jpg","year":"2004","rating":8.0,"genres":["Action","Crime","Thriller"],"overview":"The Bride continues her quest of revenge against her former boss and colleagues."},
    {"id": 157336, "title":"Interstellar","poster_path":"/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg","backdrop_path":"/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg","year":"2014","rating":8.4,"genres":["Adventure","Drama","Sci-Fi"],"overview":"A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."},
    {"id": 453395, "title":"Doctor Strange in the Multiverse of Madness","poster_path":"/9Gtg2DzB5YAMKmR0uN7nJPTNLL.jpg","backdrop_path":"/2MT3ZjZ6Yl2Yrhq2tC1KHqPGR7.jpg","year":"2022","rating":7.3,"genres":["Action","Adventure","Fantasy"],"overview":"Doctor Strange teams up with a mysterious teenage girl to travel across multiverses."},
    {"id": 299536, "title":"Avengers: Infinity War","poster_path":"/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg","backdrop_path":"/bOGkgRGdhnBYIIYzQkR5MpGEDD.jpg","year":"2018","rating":8.3,"genres":["Action","Adventure","Sci-Fi"],"overview":"The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos."},
    {"id": 299534, "title":"Avengers: Endgame","poster_path":"/or06FNq42EIKQ2NsGyv2BQSDMaM.jpg","backdrop_path":"/7RyHsO4Q3QmZ8rVFXjBi8PJ0iG.jpg","year":"2019","rating":8.3,"genres":["Action","Adventure","Drama"],"overview":"After the devastating events of Infinity War, the Avengers assemble once more to reverse Thanos' actions."},
    {"id": 315162, "title":"Puss in Boots: The Last Wish","poster_path":"/kuf6dutpsT0vSVehic3EZIqkOBt.jpg","backdrop_path":"/r9PkFnRUIthgBp2RZZzDx1QvGL.jpg","year":"2022","rating":8.3,"genres":["Animation","Adventure","Comedy"],"overview":"Puss in Boots discovers that his passion for adventure has taken its toll when he learns that he is on his last life."},
    {"id": 361743, "title":"Top Gun: Maverick","poster_path":"/62HCnUTPiZpB8h3jmnAmdSf1uF.jpg","backdrop_path":"/i3LJ4R4UElM6jLxN0otQnzUUK4.jpg","year":"2022","rating":8.3,"genres":["Action","Drama"],"overview":"After more than thirty years of service as a top naval aviator, Pete Maverick encounters a new enemy."},
    {"id": 335983, "title":"Venom","poster_path":"/2uNW4WbgBXL25BAbXGLnLqX71Sw.jpg","backdrop_path":"/cGqYSvTj0XQ6Q7i9r7uKJz3K2x.jpg","year":"2018","rating":6.8,"genres":["Action","Sci-Fi","Adventure"],"overview":"When Eddie Brock acquires the powers of a symbiote, he will have to release this anti-hero being to save his life."},
    {"id": 284054, "title":"Black Panther","poster_path":"/uxzzxijgPIY7slzFvEYP0iVq8F.jpg","backdrop_path":"/3hC7rQ7vG2PxyCJ5hFMgKJ6NvF.jpg","year":"2018","rating":7.3,"genres":["Action","Adventure","Sci-Fi"],"overview":"After his father's death, T'Challa returns home to the hidden kingdom of Wakanda to take his rightful place as king."},
    {"id": 438631, "title":"Dune","poster_path":"/d5NXSklXo0qyIYkgV94XAgMIckC.jpg","backdrop_path":"/jYEW5xZkZk2WTrJMG8Pq7P6VqP.jpg","year":"2021","rating":7.8,"genres":["Sci-Fi","Adventure","Action"],"overview":"Paul Atreides, a brilliant and gifted young man born into a great destiny beyond his understanding, must travel to the most dangerous planet in the universe."},
    {"id": 508947, "title":"Turning Red","poster_path":"/qsdjk9oAKSQMWs0Vt5Pyfh6OII.jpg","backdrop_path":"/fZI1k1gHrM0EHg7fXGuDE1x1UM.jpg","year":"2022","rating":7.5,"genres":["Animation","Comedy","Family"],"overview":"A thirteen-year-old girl turns into a giant red panda whenever she gets too excited."},
    {"id": 361743, "title":"Top Gun: Maverick","poster_path":"/62HCnUTPiZpB8h3jmnAmdSf1uF.jpg","backdrop_path":"/i3LJ4R4UElM6jLxN0otQnzUUK4.jpg","year":"2022","rating":8.3,"genres":["Action","Drama"],"overview":"After thirty years of service, Maverick confronts drones and old ghosts in a high-stakes mission."},
    {"id": 569094, "title":"Spider-Man: Across the Spider-Verse","poster_path":"/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg","backdrop_path":"/nGxUxi3PfXDRmBq90tqwnYeASJ.jpg","year":"2023","rating":8.4,"genres":["Animation","Action","Adventure"],"overview":"Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its existence."},
    {"id": 502356, "title":"The Super Mario Bros. Movie","poster_path":"/qNBAXBIQlnOThrVvA6mA2K4g1N.jpg","backdrop_path":"/9n2tJBplPbgR2caH3yjsC3BFSj.jpg","year":"2023","rating":7.5,"genres":["Animation","Adventure","Comedy"],"overview":"A Brooklyn plumber is transported to a magical world and must save a princess from a ruthless fire-breathing turtle."},
    {"id": 615656, "title":"Meg 2: The Trench","poster_path":"/4m1Au3YkjqsxF8iwQGPX3L2cM6.jpg","backdrop_path":"/8Yz1VN5VLw7T1BC6n3bKz6YTQK.jpg","year":"2023","rating":6.8,"genres":["Action","Sci-Fi","Horror"],"overview":"A research team encounters multiple threats as they explore the deepest parts of the ocean."},
    {"id": 976573, "title":"Elemental","poster_path":"/6eTOY5gNmsvDNJwpTHhBL4gPrER.jpg","backdrop_path":"/zXI9NVsK6EzG5h0VLDnTHSNkQf.jpg","year":"2023","rating":7.3,"genres":["Animation","Comedy","Family"],"overview":"In a city where fire, water, land and air residents live together, a fiery young woman and a go-with-the-flow guy discover something elemental."},
    {"id": 693134, "title":"Dune: Part Two","poster_path":"/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg","backdrop_path":"/ohQ0XJVqV5fskH2dC7jhYiOC5I.jpg","year":"2024","rating":8.5,"genres":["Sci-Fi","Action","Adventure"],"overview":"Paul Atreides unites with the Fremen to seek revenge against those who destroyed his family."},
]

FALLBACK_TV = [
    {"id": 1396, "name":"Breaking Bad","poster_path":"/ztkUQ2GSsW0OCPYoFyKjTcBBe8.jpg","backdrop_path":"/3vy1l3F4HOKjq3fYjnEnqQ8Hm6.jpg","year":"2008","rating":8.9,"genres":["Crime","Drama","Thriller"],"overview":"A high school chemistry teacher diagnosed with inoperable lung cancer turns to manufacturing and selling methamphetamine."},
    {"id": 1399, "name":"Game of Thrones","poster_path":"/u3bZgnGQ9T01s05T3Cj3jCj6cQ.jpg","backdrop_path":"/suH4g4L6D7wZ6Z6Z6Z6Z6Z6Z6Z6.jpg","year":"2011","rating":8.4,"genres":["Action","Adventure","Drama"],"overview":"Nine noble families fight for control over the lands of Westeros."},
]

FALLBACK_TRAILERS = {
    550: "SUXWAEX2jlg", 680: "s7EdQ4FqbhY", 238: "sY1S34973zA", 155: "EXeTwQWrcwY",
    244786: "7d_jQycdQGo", 11: "vZ734NWnAHA", 497: "Ki4haFrqSrw", 807: "znmZoVkCjpI",
    278: "6hB3S9bIaco", 27205: "YoHD9XEInc0", 769: "2ilzidi_J8Q", 13: "bLvqoHBptjg",
    24: "7kSuas6mRpk", 393: "0a5wXj0J3s", 157336: "zSWdZVtXT7E",
    299536: "QwievZPc8kU", 299534: "TcMBFSGVi1c", 315162: "RqrXhwS33yc",
    361743: "giXco2jaZ_4", 335983: "u9Mv98Gr5pY", 284054: "dxWvtMOGAhw",
    438631: "8g18jFHCLXk", 508947: "XdKzUbAiswE", 569094: "shW9i6k8cB0",
    502356: "TnGl01FkR0Q", 615656: "mKeGMOcPR5I", 976573: "fX_Q7TqzY7E",
    693134: "Way9Dexny3w",
}

def build_fallback_movie(m, genre_ids_str="Drama"):
    tid = m["id"]
    yt_key = FALLBACK_TRAILERS.get(tid)
    trailer = f"https://www.youtube.com/embed/{yt_key}?autoplay=1" if yt_key else None
    streaming = [
        f"https://embed.su/embed/movie/{tid}",
        f"https://vidsrc.to/embed/movie/{tid}",
        f"https://www.2embed.cc/embed/{tid}",
        f"https://multiembed.mov/?video_id={tid}&tmdb=1",
    ]
    primary = trailer or streaming[0]
    sources = []
    if trailer:
        sources.append(trailer)
    sources.extend(streaming)
    return {
        "id": tid,
        "title": m["title"],
        "poster": f"{IMG_BASE}{m['poster_path']}",
        "backdrop": f"{IMG_BASE}{m['backdrop_path']}",
        "year": m.get("year", ""),
        "rating": m.get("rating", 0),
        "overview": m.get("overview", ""),
        "media_type": "movie",
        "genres": m.get("genres", [genre_ids_str]),
        "embed_url": primary,
        "embed_sources": sources,
    }

def build_fallback_tv(t):
    tid = t["id"]
    streaming = [
        f"https://embed.su/embed/tv/{tid}/1/1",
        f"https://vidsrc.to/embed/tv/{tid}/1/1",
        f"https://www.2embed.cc/embed/{tid}?s=1&e=1",
        f"https://multiembed.mov/?video_id={tid}&tmdb=1&s=1&e=1",
    ]
    return {
        "id": t["id"],
        "title": t["name"],
        "poster": f"{IMG_BASE}{t['poster_path']}",
        "backdrop": f"{IMG_BASE}{t['backdrop_path']}",
        "year": t.get("year", ""),
        "rating": t.get("rating", 0),
        "overview": t.get("overview", ""),
        "media_type": "tv",
        "genres": t.get("genres", []),
        "embed_url": streaming[0],
        "embed_sources": streaming,
    }

FALLBACK_SECTIONS = [
    {"genre":"Action", "movies":[build_fallback_movie(FALLBACK_MOVIES[i]) for i in [4,7,10,12,17,18,22]]},
    {"genre":"Comedy", "movies":[build_fallback_movie(FALLBACK_MOVIES[i]) for i in [11,18,23,26,28]]},
    {"genre":"Drama", "movies":[build_fallback_movie(FALLBACK_MOVIES[i]) for i in [0,2,6,8,10,13]]},
    {"genre":"Sci-Fi", "movies":[build_fallback_movie(FALLBACK_MOVIES[i]) for i in [4,9,14,16,17,21,24,29]]},
    {"genre":"Thriller", "movies":[build_fallback_movie(FALLBACK_MOVIES[i]) for i in [7,12,0]]},
    {"genre":"Animation", "movies":[build_fallback_movie(FALLBACK_MOVIES[i]) for i in [18,23,25,26,27]]},
    {"genre":"Romance", "movies":[build_fallback_movie(FALLBACK_MOVIES[i]) for i in [11]]},
    {"genre":"Horror", "movies":[build_fallback_movie(FALLBACK_MOVIES[i]) for i in [27]]},
]

def get_fallback_home():
    trending = [build_fallback_movie(FALLBACK_MOVIES[i]) for i in [0,1,2,3,4,5,6,7,8,9]]
    return {"trending": trending, "sections": FALLBACK_SECTIONS}

def get_fallback_search(q):
    ql = q.lower()
    results = []
    for m in FALLBACK_MOVIES:
        if ql in m["title"].lower():
            results.append(build_fallback_movie(m))
            if len(results) >= 8:
                break
    for t in FALLBACK_TV:
        if ql in t["name"].lower():
            results.append(build_fallback_tv(t))
            if len(results) >= 8:
                break
    return results

def get_fallback_trending():
    return [build_fallback_movie(FALLBACK_MOVIES[i]) for i in range(min(20, len(FALLBACK_MOVIES)))]

def get_fallback_genre(genre_id):
    genre_name = {v: k for k, v in GENRE_IDS.items()}.get(genre_id, "")
    if not genre_name:
        return []
    for sec in FALLBACK_SECTIONS:
        if sec["genre"].lower() == genre_name.lower():
            return sec["movies"]
    return []

def get_fallback_recommendations(content_id):
    results = []
    for m in FALLBACK_MOVIES:
        if m["id"] != content_id:
            results.append(build_fallback_movie(m))
        if len(results) >= 12:
            break
    return results[:12]

def movie_embed(tmdb_id, imdb_id=None):
    yt_key = FALLBACK_TRAILERS.get(tmdb_id)
    trailer = f"https://www.youtube.com/embed/{yt_key}?autoplay=1" if yt_key else None
    streaming = [
        f"https://embed.su/embed/movie/{tmdb_id}",
        f"https://vidsrc.to/embed/movie/{tmdb_id}",
        f"https://www.2embed.cc/embed/{tmdb_id}",
        f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1",
    ]
    primary = trailer or streaming[0]
    sources = []
    if trailer:
        sources.append(trailer)
    sources.extend(streaming)
    return primary, sources

def tv_embed(tmdb_id, season, episode):
    sources = [
        f"https://embed.su/embed/tv/{tmdb_id}/{season}/{episode}",
        f"https://vidsrc.to/embed/tv/{tmdb_id}/{season}/{episode}",
        f"https://www.2embed.cc/embed/{tmdb_id}?s={season}&e={episode}",
        f"https://multiembed.mov/?video_id={tmdb_id}&tmdb=1&s={season}&e={episode}",
    ]
    return sources[0], sources

def build_movie(m):
    genres = []
    if "genre_ids" in m:
        id_to_name = {v: k for k, v in GENRE_IDS.items()}
        genres = [id_to_name.get(gid) for gid in m.get("genre_ids", []) if id_to_name.get(gid)]
    tid = m["id"]
    yt_key = FALLBACK_TRAILERS.get(tid)
    trailer = f"https://www.youtube.com/embed/{yt_key}?autoplay=1" if yt_key else None
    streaming = [
        f"https://embed.su/embed/movie/{tid}",
        f"https://vidsrc.to/embed/movie/{tid}",
        f"https://www.2embed.cc/embed/{tid}",
        f"https://multiembed.mov/?video_id={tid}&tmdb=1",
    ]
    primary = trailer or streaming[0]
    sources = []
    if trailer:
        sources.append(trailer)
    sources.extend(streaming)
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
    streaming = [
        f"https://embed.su/embed/tv/{tid}/1/1",
        f"https://vidsrc.to/embed/tv/{tid}/1/1",
        f"https://www.2embed.cc/embed/{tid}?s=1&e=1",
        f"https://multiembed.mov/?video_id={tid}&tmdb=1&s=1&e=1",
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
        "genres": [],
        "embed_url": streaming[0],
        "embed_sources": streaming,
    }
    return item

@app.get("/")
async def index():
    return {"message": "MovieBox API - Live"}

@app.get("/search")
def search(q: str = "", limit: int = 10):
    if not q.strip():
        return []
    d = tmdb_get("search/multi", {"query": q, "language": "en-US", "page": 1})
    if d.get("results"):
        results = d.get("results", [])[:limit]
        out = []
        for r in results:
            if r.get("media_type") == "movie":
                out.append(build_movie(r))
            elif r.get("media_type") == "tv":
                out.append(build_tv(r))
        return out
    return get_fallback_search(q)

@app.get("/trending")
def trending(media_type: str = "movie", limit: int = 20):
    d = tmdb_get(f"trending/{media_type}/week", {"language": "en-US"})
    if d.get("results"):
        results = d.get("results", [])[:limit]
        if media_type == "tv":
            return [build_tv(t) for t in results]
        return [build_movie(m) for m in results]
    return get_fallback_trending()

@app.get("/movie/{movie_id}")
def movie_detail(movie_id: int):
    d = tmdb_get(f"movie/{movie_id}", {"language": "en-US"})
    if d and "title" in d:
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
    for m in FALLBACK_MOVIES:
        if m["id"] == movie_id:
            fb = build_fallback_movie(m)
            fb["embed_url"] = f"https://www.youtube.com/embed/{FALLBACK_TRAILERS.get(movie_id, 'dQw4w9WgXcQ')}?autoplay=1"
            fb["embed_sources"] = [fb["embed_url"]]
            return fb
    return {"error": "Movie not found"}

@app.get("/tv/{tv_id}")
def tv_detail(tv_id: int):
    d = tmdb_get(f"tv/{tv_id}", {"language": "en-US"})
    if d and "name" in d:
        seasons = []
        for s in d.get("seasons", []):
            if s["season_number"] > 0:
                seasons.append({"season": s["season_number"], "episodes": s.get("episode_count", 0), "poster": f"{IMG_BASE}{s['poster_path']}" if s.get("poster_path") else None})
        primary, sources = tv_embed(d["id"], 1, 1)
        return {"id": d["id"], "title": d.get("name", ""), "poster": f"{IMG_BASE}{d['poster_path']}" if d.get("poster_path") else None, "backdrop": f"{IMG_BASE}{d['backdrop_path']}" if d.get("backdrop_path") else None, "year": (d.get("first_air_date") or "")[:4], "rating": round(d.get("vote_average", 0), 1), "overview": d.get("overview", ""), "media_type": "tv", "seasons": seasons, "embed_url": primary, "embed_sources": sources}
    for t in FALLBACK_TV:
        if t["id"] == tv_id:
            return {**build_fallback_tv(t), "seasons": []}
    return {"error": "TV show not found"}

@app.get("/tv/{tv_id}/season/{season_num}")
def tv_season(tv_id: int, season_num: int):
    d = tmdb_get(f"tv/{tv_id}/season/{season_num}", {"language": "en-US"})
    if d and "episodes" in d:
        episodes = []
        for ep in d.get("episodes", []):
            primary, sources = tv_embed(tv_id, season_num, ep["episode_number"])
            episodes.append({"id": ep["id"], "episode": ep["episode_number"], "title": ep["name"], "overview": ep.get("overview", ""), "still": f"{IMG_BASE}{ep['still_path']}" if ep.get("still_path") else None, "rating": round(ep.get("vote_average", 0), 1), "embed_url": primary, "embed_sources": sources})
        return {"show_id": tv_id, "season": season_num, "episodes": episodes}
    return {"error": "Season not found"}

@app.get("/genre/{genre_id}")
def by_genre(genre_id: int, page: int = 1):
    d = tmdb_get("discover/movie", {"with_genres": genre_id, "sort_by": "popularity.desc", "page": page, "language": "en-US"})
    if d.get("results"):
        return [build_movie(m) for m in d.get("results", [])]
    return get_fallback_genre(genre_id)

@app.get("/recommendations/{media_type}/{content_id}")
def recommendations(media_type: str, content_id: int):
    d = tmdb_get(f"{media_type}/{content_id}/recommendations", {"language": "en-US"})
    if d.get("results"):
        results = d.get("results", [])[:12]
        if media_type == "tv":
            return [build_tv(t) for t in results]
        return [build_movie(m) for m in results]
    return get_fallback_recommendations(content_id)

@app.get("/music")
def music(page: int = 1):
    d = tmdb_get("discover/movie", {"with_genres": "10402", "sort_by": "popularity.desc", "page": page, "language": "en-US"})
    if d.get("results"):
        return [build_movie(m) for m in d.get("results", [])]
    return [build_fallback_movie(FALLBACK_MOVIES[i]) for i in [4, 11, 18, 23, 26, 28]]

@app.get("/short-videos")
def short_videos():
    results = get_fallback_trending()[:10]
    items = []
    for m in results:
        yt_key = FALLBACK_TRAILERS.get(m["id"])
        if yt_key:
            items.append({"id": m["id"], "title": m["title"], "poster": m["poster"], "year": m["year"], "rating": m["rating"], "trailer_key": yt_key, "embed_url": f"https://www.youtube.com/embed/{yt_key}?autoplay=1"})
    return items

@app.get("/hero-content")
def hero_content(limit: int = 10):
    d = tmdb_get("trending/movie/week", {"language": "en-US"})
    if d.get("results"):
        results = d.get("results", [])[:limit]
        items = []
        for m in results:
            items.append({"id": m["id"], "title": m["title"], "poster": f"{IMG_BASE}{m['poster_path']}" if m.get("poster_path") else None, "backdrop": f"{IMG_BASE}{m['backdrop_path']}" if m.get("backdrop_path") else None, "year": (m.get("release_date") or "")[:4], "rating": round(m.get("vote_average", 0), 1), "overview": m.get("overview", "")})
        return items
    return [{"id": m["id"], "title": m["title"], "poster": f"{IMG_BASE}{m['poster_path']}", "backdrop": f"{IMG_BASE}{m['backdrop_path']}", "year": m["year"], "rating": m["rating"], "overview": m["overview"]} for m in FALLBACK_MOVIES[:10]]

@app.get("/all-movies")
def all_movies(page: int = 1):
    d = tmdb_get("discover/movie", {"sort_by": "popularity.desc", "page": page, "language": "en-US"})
    if d.get("results"):
        return [build_movie(m) for m in d.get("results", [])]
    return get_fallback_trending()

HOME_GENRES = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Thriller", "Animation"]

@app.get("/home")
def home_page():
    d = tmdb_get("trending/movie/week", {"language": "en-US"})
    if d.get("results"):
        result = {"trending": [], "sections": []}
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
    return get_fallback_home()


