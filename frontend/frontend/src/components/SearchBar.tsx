import { useState } from 'react';
import axios from 'axios';

interface Track {
  id: string;
  title: string;
  artist: string;
  album_art: string | null;
  preview_url?: string | null;
}

interface Props {
  onSelect: (spotifyId: string) => void;
}
export default function SearchBar({ onSelect }: Props) {
  const [searchResults, setSearchResults] = useState<Track[]>([]);

  const handleSearch = async (title: string) => {
    const response = await axios.get(`http://localhost:8080/api/v1/spotify/search?track_title=${title}`);
    setSearchResults(response.data.results);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search for a track title..."      
        onKeyDown={(e) => {
            if (e.key === 'Enter') {
                const val = e.currentTarget.value.trim();
                if (val !== '') {
                    handleSearch(val);
                } else {
                    setSearchResults([]);
                }
            }
        }}
      />
      {searchResults.length > 0 && (
        <div>
          {searchResults.map((track) => (
            <div key={track.id} onClick={() => {
              onSelect(track.id);
              setSearchResults([]);
            }}>
              {track.album_art && <img src={track.album_art} alt={track.title} />}
              <div>
                <div>{track.title}</div>
                <div>{track.artist}</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
