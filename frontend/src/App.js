import React, { useState, useEffect, useRef, useCallback } from "react";
import "./App.css";

const API = process.env.NODE_ENV === "production" ? "" : "http://127.0.0.1:8000";

const GENRES = [
  "All", "Action", "Adventure", "Animation", "Comedy", "Crime",
  "Documentary", "Drama", "Fantasy", "Horror", "Music", "Mystery",
  "Romance", "Sci-Fi", "Thriller", "War"
];

const GENRE_IDS = {
  Action: 28, Adventure: 12, Animation: 16, Comedy: 35,
  Crime: 80, Documentary: 99, Drama: 18, Fantasy: 14,
  Horror: 27, Music: 10402, Mystery: 9648, Romance: 10749,
  "Sci-Fi": 878, Thriller: 53, War: 10752
};

const NAV_TABS = ["Movies", "TV Series", "Music", "Short Videos"];

const GENRE_GRADIENT = {
  Action: "linear-gradient(135deg, #c0392b, #8e2424)",
  Adventure: "linear-gradient(135deg, #16a085, #0e6655)",
  Animation: "linear-gradient(135deg, #6c5ce7, #4834d4)",
  Comedy: "linear-gradient(135deg, #fdcb6e, #e17055)",
  Crime: "linear-gradient(135deg, #2c3e50, #34495e)",
  Documentary: "linear-gradient(135deg, #74b9ff, #0984e3)",
  Drama: "linear-gradient(135deg, #2c3e50, #4a6278)",
  Fantasy: "linear-gradient(135deg, #a29bfe, #6c5ce7)",
  Horror: "linear-gradient(135deg, #2d3436, #636e72)",
  Music: "linear-gradient(135deg, #fd79a8, #e84393)",
  Mystery: "linear-gradient(135deg, #6c5ce7, #2d3436)",
  Romance: "linear-gradient(135deg, #fd79a8, #fab1a0)",
  "Sci-Fi": "linear-gradient(135deg, #0984e3, #2d3436)",
  Thriller: "linear-gradient(135deg, #d63031, #2d3436)",
  War: "linear-gradient(135deg, #636e72, #2d3436)",
  default: "linear-gradient(135deg, #141e30, #243b55)",
};

function App() {
  const [activeTab, setActiveTab] = useState("Movies");
  const [trendingMovies, setTrendingMovies] = useState([]);
  const [sections, setSections] = useState([]);
  const [genreMovies, setGenreMovies] = useState([]);
  const [tvShows, setTvShows] = useState([]);
  const [musicContent, setMusicContent] = useState([]);
  const [shortVideos, setShortVideos] = useState([]);
  const [searchInput, setSearchInput] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [searchOpen, setSearchOpen] = useState(false);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [contentLoading, setContentLoading] = useState(false);
  const [error, setError] = useState("");
  const [player, setPlayer] = useState(null);
  const [playerSeason, setPlayerSeason] = useState(1);
  const [playerEpisode, setPlayerEpisode] = useState(1);
  const [tvSeasons, setTvSeasons] = useState([]);
  const [tvEpisodes, setTvEpisodes] = useState([]);
  const [activeGenre, setActiveGenre] = useState("All");
  const [menuOpen, setMenuOpen] = useState(false);
  const [heroIndex, setHeroIndex] = useState(0);
  const searchRef = useRef(null);

  useEffect(() => {
    setLoading(true);
    setError("");
    fetch(`${API}/home`)
      .then((r) => { if (!r.ok) throw new Error("Backend unavailable"); return r.json(); })
      .then((data) => {
        setTrendingMovies(data.trending || []);
        setSections(data.sections || []);
      })
      .catch(() => setError("Could not connect to server. Make sure backend is running."))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (trendingMovies.length < 2) return;
    const t = setInterval(() => {
      setHeroIndex((i) => (i + 1) % trendingMovies.length);
    }, 5000);
    return () => clearInterval(t);
  }, [trendingMovies.length]);

  useEffect(() => {
    const handleClick = (e) => {
      if (searchRef.current && !searchRef.current.contains(e.target)) {
        setSearchOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, []);

  useEffect(() => {
    if (!searchInput.trim()) { setSearchResults([]); return; }
    const timer = setTimeout(async () => {
      try {
        const r = await fetch(`${API}/search?q=${encodeURIComponent(searchInput)}&limit=8`);
        setSearchResults(await r.json());
        setSearchOpen(true);
      } catch { setSearchResults([]); }
    }, 300);
    return () => clearTimeout(timer);
  }, [searchInput]);

  const switchTab = useCallback(async (tab) => {
    setActiveTab(tab);
    setActiveGenre("All");
    setSelectedMovie(null);
    setRecommendations([]);
    if (tab === "Movies") return;
    setContentLoading(true);
    try {
      let data;
      if (tab === "TV Series") {
        const r = await fetch(`${API}/trending?media_type=tv&limit=50`);
        data = await r.json();
        setTvShows(data || []);
      } else if (tab === "Music") {
        const r = await fetch(`${API}/music?page=1`);
        data = await r.json();
        setMusicContent(data || []);
      } else if (tab === "Short Videos") {
        const r = await fetch(`${API}/short-videos`);
        data = await r.json();
        setShortVideos(data || []);
      }
    } catch {}
    setContentLoading(false);
  }, []);

  const loadGenre = useCallback(async (genre) => {
    setActiveGenre(genre);
    setMenuOpen(false);
    setActiveTab("Movies");
    setSelectedMovie(null);
    setRecommendations([]);
    if (genre === "All") {
      setGenreMovies([]);
      return;
    }
    setContentLoading(true);
    try {
      const gid = GENRE_IDS[genre];
      if (gid) {
        const r = await fetch(`${API}/genre/${gid}?page=1`);
        setGenreMovies(await r.json());
      }
    } catch {}
    setContentLoading(false);
  }, []);

  const handleSearchSelect = async (item) => {
    setSearchInput(item.title);
    setSearchOpen(false);
    setActiveTab("Movies");
    setActiveGenre("All");
    setGenreMovies([]);
    setSelectedMovie(item);
    setContentLoading(true);
    try {
      const r = await fetch(`${API}/recommendations/${item.media_type}/${item.id}`);
      setRecommendations(await r.json());
    } catch {}
    setContentLoading(false);
  };

  const getGradient = (genres) => {
    if (!genres || !genres.length) return GENRE_GRADIENT.default;
    for (const g of genres) {
      if (GENRE_GRADIENT[g]) return GENRE_GRADIENT[g];
    }
    return GENRE_GRADIENT.default;
  };

  const getInitials = (title) => {
    return title.replace(/\([^)]*\)/g, "").trim().split(" ").slice(0, 2).map((w) => w[0] || "").join("").toUpperCase();
  };

  const scrollRow = (id, dir) => {
    const el = document.getElementById(id);
    if (el) el.scrollBy({ left: dir * 800, behavior: "smooth" });
  };

  const openMoviePlayer = (movie) => {
    if (movie.embed_url) {
      setPlayer({ ...movie, media_type: "movie" });
      document.body.style.overflow = "hidden";
    }
  };

  const openTvPlayer = async (tv) => {
    if (!tv.embed_url) return;
    setPlayer({ ...tv, media_type: "tv" });
    document.body.style.overflow = "hidden";
    setPlayerSeason(1);
    setPlayerEpisode(1);
    try {
      const r = await fetch(`${API}/tv/${tv.id}`);
      const data = await r.json();
      if (data.seasons) setTvSeasons(data.seasons);
      const r2 = await fetch(`${API}/tv/${tv.id}/season/1`);
      const eps = await r2.json();
      if (eps.episodes) setTvEpisodes(eps.episodes);
    } catch {}
  };

  const changeTvSeason = async (season) => {
    setPlayerSeason(season);
    setPlayerEpisode(1);
    if (player) {
      try {
        const r = await fetch(`${API}/tv/${player.id}/season/${season}`);
        const data = await r.json();
        if (data.episodes && data.episodes.length > 0) {
          setTvEpisodes(data.episodes);
          setPlayerEpisode(data.episodes[0].episode);
          setPlayer((prev) => ({
            ...prev,
            embed_url: data.episodes[0].embed_url,
            embed_sources: data.episodes[0].embed_sources,
          }));
        }
      } catch {}
    }
  };

  const changeTvEpisode = (episode) => {
    setPlayerEpisode(episode);
    if (player) {
      const ep = tvEpisodes.find((e) => e.episode === episode);
      if (ep) {
        setPlayer((prev) => ({
          ...prev,
          embed_url: ep.embed_url,
          embed_sources: ep.embed_sources,
        }));
      }
    }
  };

  const openShortVideoPlayer = (video) => {
    setPlayer({
      id: video.id,
      title: video.title,
      embed_url: video.embed_url,
      embed_sources: [video.embed_url],
      media_type: "short",
    });
    document.body.style.overflow = "hidden";
  };

  const closePlayer = () => {
    setPlayer(null);
    setTvSeasons([]);
    setTvEpisodes([]);
    document.body.style.overflow = "";
  };

  const renderPoster = (movie, cls = "poster-img", initialsCls = "poster-initials") => {
    if (movie.poster) {
      return <img src={movie.poster} alt={movie.title} className={cls} loading="lazy" />;
    }
    return <span className={initialsCls}>{getInitials(movie.title)}</span>;
  };

  const renderCards = (movies, rowId, onClick) => (
    <div className="card-row-wrapper">
      <button className="row-arrow row-arrow-left" onClick={() => scrollRow(rowId, -1)}>‹</button>
      <div className="card-row" id={rowId}>
        {movies.map((movie, i) => (
          <div key={i} className="poster-card" onClick={() => onClick(movie)}>
            <div className="poster-frame" style={{ background: getGradient(movie.genres || []) }}>
              {renderPoster(movie)}
              <div className="poster-overlay">
                <div className="poster-play">
                  <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </div>
                <div className="poster-info">
                  <p className="poster-title">{movie.title}</p>
                  <p className="poster-genres">
                    {movie.genres ? movie.genres.slice(0, 3).join(" • ") : ""}
                  </p>
                </div>
              </div>
              {movie.rating > 0 && <span className="poster-rating">★ {movie.rating}</span>}
              {movie.year && <span className="poster-year">{movie.year}</span>}
            </div>
          </div>
        ))}
      </div>
      <button className="row-arrow row-arrow-right" onClick={() => scrollRow(rowId, 1)}>›</button>
    </div>
  );

  const hero = trendingMovies[heroIndex] || null;

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-left">
          <div className="nav-logo">
            <span className="logo-m">M</span>
            <span className="logo-text">ovie<span className="logo-accent">Box</span></span>
          </div>
        </div>
        <div className="nav-tabs">
          {NAV_TABS.map((tab) => (
            <button
              key={tab}
              className={`nav-tab ${activeTab === tab ? "active" : ""}`}
              onClick={() => switchTab(tab)}
            >
              {tab}
            </button>
          ))}
        </div>
        <div className="nav-center" ref={searchRef}>
          <div className="search-wrap">
            <svg className="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="7" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              type="text" placeholder="Search movies, TV shows..." className="search-input"
              value={searchInput} onChange={(e) => setSearchInput(e.target.value)}
              onFocus={() => searchResults.length > 0 && setSearchOpen(true)}
              onKeyDown={(e) => { if (e.key === "Enter" && searchInput.trim() && searchResults.length > 0) handleSearchSelect(searchResults[0]); }}
            />
            {searchOpen && searchResults.length > 0 && (
              <div className="search-dropdown">
                {searchResults.slice(0, 8).map((m, i) => (
                  <div key={i} className="search-item" onClick={() => handleSearchSelect(m)}>
                    <div className="search-item-thumb" style={{ background: getGradient(m.genres || []) }}>
                      {getInitials(m.title)}
                    </div>
                    <div className="search-item-info">
                      <div className="search-item-title">{m.title}</div>
                      <div className="search-item-meta">{m.media_type === "tv" ? "TV Series" : "Movie"}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        <div className="nav-right">
          <button className="nav-genre-btn" onClick={() => setMenuOpen(!menuOpen)}>
            Genre
            <svg viewBox="0 0 24 24" fill="currentColor" width="12" height="12"><path d="M7 10l5 5 5-5z" /></svg>
          </button>
          {menuOpen && (
            <div className="genre-menu" onMouseLeave={() => setMenuOpen(false)}>
              {GENRES.map((g) => (
                <div key={g} className={`genre-menu-item ${activeGenre === g ? "active" : ""}`}
                  onClick={() => loadGenre(g)}>
                  {g}
                </div>
              ))}
            </div>
          )}
        </div>
      </nav>

      {loading ? (
        <section className="hero">
          <div className="hero-bg" style={{ background: "linear-gradient(135deg, #141e30, #243b55)" }}>
            <div className="hero-gradient-overlay" />
          </div>
          <div className="hero-content">
            <div className="hero-badge" style={{ background: "rgba(255,255,255,0.1)", border: "none", color: "transparent" }}>LOADING</div>
            <h1 className="hero-title" style={{ background: "rgba(255,255,255,0.08)", height: "40px", width: "60%", borderRadius: "6px", marginBottom: "14px" }} />
            <div style={{ display: "flex", gap: "14px", marginBottom: "14px" }}>
              <span style={{ background: "rgba(255,255,255,0.06)", height: "12px", width: "80px", borderRadius: "4px" }} />
              <span style={{ background: "rgba(255,255,255,0.06)", height: "12px", width: "60px", borderRadius: "4px" }} />
            </div>
            <p style={{ background: "rgba(255,255,255,0.06)", height: "60px", width: "50%", borderRadius: "6px" }} />
          </div>
        </section>
      ) : error ? (
        <section className="hero">
          <div className="hero-bg" style={{ background: "linear-gradient(135deg, #141e30, #243b55)" }}>
            <div className="hero-gradient-overlay" />
          </div>
          <div className="hero-content">
            <div className="hero-badge" style={{ background: "rgba(229,9,20,0.2)", border: "1px solid rgba(229,9,20,0.4)" }}>ERROR</div>
            <h1 className="hero-title" style={{ fontSize: "28px" }}>Cannot connect to server</h1>
            <p className="hero-desc">{error}</p>
            <div className="hero-actions">
              <button className="btn-watch" onClick={() => window.location.reload()}>Retry</button>
            </div>
          </div>
        </section>
      ) : hero && activeTab === "Movies" && !selectedMovie && activeGenre === "All" && (
        <section className="hero">
          <div className="hero-bg" style={{
            backgroundImage: hero.backdrop ? `url(${hero.backdrop})` : getGradient([]),
            backgroundSize: "cover", backgroundPosition: "center"
          }}>
            <div className="hero-gradient-overlay" />
            <div className="hero-dots">
              {trendingMovies.map((_, i) => (
                <span key={i} className={`hero-dot ${i === heroIndex ? "active" : ""}`} onClick={() => setHeroIndex(i)} />
              ))}
            </div>
          </div>
          <div className="hero-content">
            <div className="hero-badge">TRENDING NOW</div>
            <h1 className="hero-title">{hero.title}</h1>
            <div className="hero-meta">
              <span className="hero-rating">★ {hero.rating}</span>
              <span className="hero-year">{hero.year}</span>
            </div>
            <p className="hero-desc">{hero.overview?.slice(0, 200)}</p>
            <div className="hero-actions">
              <button className="btn-watch" onClick={() => openMoviePlayer(hero)}>
                <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M8 5v14l11-7z" /></svg>
                Watch Now
              </button>
            </div>
          </div>
          <button className="hero-arrow hero-arrow-left" onClick={() => setHeroIndex((i) => (i - 1 + trendingMovies.length) % trendingMovies.length)}>‹</button>
          <button className="hero-arrow hero-arrow-right" onClick={() => setHeroIndex((i) => (i + 1) % trendingMovies.length)}>›</button>
        </section>
      )}

      <main className="main-content">
        {activeTab === "Movies" && !selectedMovie && activeGenre === "All" && (
          <>
            {sections.map((sec, i) => (
              <section key={sec.genre} className="section hero-spacer">
                <div className="section-head">
                  <h2>{sec.genre}</h2>
                </div>
                {sec.movies.length > 0
                  ? renderCards(sec.movies, `sec-${i}`, openMoviePlayer)
                  : <div className="card-row">{[1,2,3,4,5,6].map((k) => <div key={k} className="poster-frame skeleton" />)}</div>
                }
              </section>
            ))}
          </>
        )}

        {activeTab === "Movies" && activeGenre !== "All" && (
          <section className="section hero-spacer">
            <div className="section-head"><h2>{activeGenre}</h2></div>
            {contentLoading ? (
              <div className="card-row">{[1,2,3,4,5,6].map((i) => <div key={i} className="poster-frame skeleton" />)}
              </div>
            ) : genreMovies.length > 0 ? renderCards(genreMovies, "genre-row", openMoviePlayer) : (
              <div className="coming-soon">No movies found.</div>
            )}
          </section>
        )}

        {activeTab === "Movies" && selectedMovie && (
          <section className="section hero-spacer">
            <div className="section-head">
              <h2>Recommendations</h2>
              <span className="section-sub">Based on "{selectedMovie.title}"</span>
            </div>
            {contentLoading ? (
              <div className="card-row">{[1,2,3,4,5,6].map((i) => <div key={i} className="poster-frame skeleton" />)}
              </div>
            ) : recommendations.length > 0 ? renderCards(recommendations, "rec-row", openMoviePlayer) : (
              <div className="coming-soon">No recommendations found.</div>
            )}
          </section>
        )}

        {activeTab === "TV Series" && (
          <section className="section hero-spacer">
            <div className="section-head"><h2>Trending TV Series</h2></div>
            {contentLoading ? (
              <div className="card-row">{[1,2,3,4,5,6].map((i) => <div key={i} className="poster-frame skeleton" />)}
              </div>
            ) : tvShows.length > 0 ? renderCards(tvShows, "tv-row", openTvPlayer) : (
              <div className="coming-soon">No TV series available.</div>
            )}
          </section>
        )}

        {activeTab === "Music" && (
          <section className="section hero-spacer">
            <div className="section-head"><h2>Music & Musicals</h2></div>
            {contentLoading ? (
              <div className="card-row">{[1,2,3,4,5,6].map((i) => <div key={i} className="poster-frame skeleton" />)}
              </div>
            ) : musicContent.length > 0 ? renderCards(musicContent, "music-row", openMoviePlayer) : (
              <div className="coming-soon">No music content available.</div>
            )}
          </section>
        )}

        {activeTab === "Short Videos" && (
          <section className="section hero-spacer">
            <div className="section-head"><h2>Trailers & Short Videos</h2></div>
            {shortVideos.length > 0 ? (
              <div className="card-row-wrapper">
                <div className="card-row" id="shorts-row">
                  {shortVideos.map((v, i) => (
                    <div key={i} className="poster-card" onClick={() => openShortVideoPlayer(v)}>
                      <div className="poster-frame" style={{ background: "#1a1a2e" }}>
                        {v.poster ? (
                          <img src={v.poster} alt={v.title} className="poster-img" loading="lazy" />
                        ) : (
                          <span className="poster-initials">{getInitials(v.title)}</span>
                        )}
                        <div className="poster-overlay">
                          <div className="poster-play">
                            <svg viewBox="0 0 24 24" fill="currentColor" width="32" height="32">
                              <path d="M8 5v14l11-7z" />
                            </svg>
                          </div>
                          <div className="poster-info">
                            <p className="poster-title">{v.title}</p>
                          </div>
                        </div>
                        {v.rating > 0 && <span className="poster-rating">★ {v.rating}</span>}
                        {v.year && <span className="poster-year">{v.year}</span>}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="coming-soon">No short videos available.</div>
            )}
          </section>
        )}

        <footer className="footer">
          <div className="footer-content">
            <div className="footer-logo">
              <span className="logo-m">M</span>
              <span className="logo-text">ovie<span className="logo-accent">Box</span></span>
            </div>
            <p className="footer-text">Powered by TMDB. This site does not host any files.</p>
          </div>
        </footer>
      </main>

      {player && (
        <div className="player-overlay" onClick={closePlayer}>
          <div className="player-container" onClick={(e) => e.stopPropagation()}>
            <div className="player-header">
              <h3>{player.title}</h3>
              <button className="player-close" onClick={closePlayer}>
                <svg viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
                </svg>
              </button>
            </div>
            {player.media_type === "tv" && (
              <div className="player-episode-bar">
                <div className="episode-controls">
                  <label>Season:</label>
                  <select value={playerSeason} onChange={(e) => changeTvSeason(Number(e.target.value))}>
                    {tvSeasons.map((s) => (
                      <option key={s.season} value={s.season}>Season {s.season}</option>
                    ))}
                  </select>
                  <label>Episode:</label>
                  <select value={playerEpisode} onChange={(e) => changeTvEpisode(Number(e.target.value))}>
                    {tvEpisodes.map((ep) => (
                      <option key={ep.episode} value={ep.episode}>
                        Episode {ep.episode}{ep.title ? ` - ${ep.title}` : ""}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            )}
            <div className="player-embed">
              <iframe
                src={player.embed_url}
                title={player.title}
                allowFullScreen
                allow="autoplay; encrypted-media; picture-in-picture"
                frameBorder="0"
              />
            </div>
            {player.embed_sources && player.embed_sources.length > 1 && (
              <div className="player-sources">
                <span className="sources-label">Server:</span>
                <div className="sources-list">
                  {player.embed_sources.map((src, i) => (
                    <button
                      key={i}
                      className={`source-btn ${src === player.embed_url ? "active" : ""}`}
                      onClick={() => setPlayer({ ...player, embed_url: src })}
                    >
                      {i === 0 && src.includes("youtube") ? "Trailer" : `Server ${i}`}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
