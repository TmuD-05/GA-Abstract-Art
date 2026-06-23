import { useState, useRef, useEffect, useCallback } from 'react';
import axios from 'axios';

interface Track {
  id: string;
  title: string;
  artist: string;
  album_art: string | null;        // 640x640 for main display
  album_art_thumb: string | null;  // 64x64 for search dropdown
  preview_url?: string | null;
}

interface Props {
  onSelect: (spotifyId: string, track: Track) => void;
}

export default function SearchBar({ onSelect }: Props) {
  const [query, setQuery] = useState<string>('');
  const [searchResults, setSearchResults] = useState<Track[]>([]);
  const [activeIndex, setActiveIndex] = useState<number>(-1);
  const [open, setOpen] = useState<boolean>(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const fetchResults = useCallback(async (title: string) => {
    if (!title.trim()) { setSearchResults([]); return; }
    try {
      const response = await axios.get(`http://localhost:8080/api/v1/spotify/search?track_title=${title}`);
      setSearchResults(response.data.results);
      setOpen(true);
      setActiveIndex(-1);
    } catch {
      setSearchResults([]);
    }
  }, []);

  const handleQueryChange = (value: string) => {
    setQuery(value);
    if (!value.trim()) {
      setSearchResults([]);
      setOpen(false);
      if (debounceRef.current) clearTimeout(debounceRef.current);
      return;
    }
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => fetchResults(value), 350);
  };

  const handleSelect = (track: Track) => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    onSelect(track.id, track);
    setQuery(`${track.title} — ${track.artist}`);
    setSearchResults([]);
    setOpen(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      if (debounceRef.current) clearTimeout(debounceRef.current);
      if (activeIndex >= 0 && searchResults[activeIndex]) {
        handleSelect(searchResults[activeIndex]);
      } else {
        fetchResults(query);
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setActiveIndex(i => Math.min(i + 1, searchResults.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setActiveIndex(i => Math.max(i - 1, -1));
    } else if (e.key === 'Escape') {
      setOpen(false);
    }
  };

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  useEffect(() => () => { if (debounceRef.current) clearTimeout(debounceRef.current); }, []);

  return (
    <div ref={containerRef} style={{ position: 'relative' }}>
      {/* Win98 sunken input */}
      <div className="win98-input-wrap">
        <input
          type="text"
          value={query}
          placeholder="Search track..."
          onChange={e => handleQueryChange(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => { if (searchResults.length > 0) setOpen(true); }}
          className="win98-input"
        />
        {query && (
          <button
            onClick={() => { setQuery(''); setSearchResults([]); setOpen(false); }}
            style={{
              background: 'none', border: 'none', cursor: 'pointer',
              padding: '0 4px', fontSize: 11, color: '#808080',
              fontFamily: 'Arial', lineHeight: 1
            }}
          >
            ✕
          </button>
        )}
      </div>

      {/* Win98 dropdown list */}
      {open && searchResults.length > 0 && (
        <div className="search-dropdown">
          {searchResults.map((track, i) => (
            <div
              key={track.id}
              onClick={() => handleSelect(track)}
              onMouseEnter={() => setActiveIndex(i)}
              className={`search-result-item${activeIndex === i ? ' active' : ''}`}
            >
              {track.album_art_thumb ? (
                <img src={track.album_art_thumb} alt={track.title} className="search-result-thumb" />
              ) : (
                <div className="search-result-thumb-empty" />
              )}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontWeight: 'bold', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {track.title}
                </div>
                <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', opacity: 0.8 }}>
                  {track.artist}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}