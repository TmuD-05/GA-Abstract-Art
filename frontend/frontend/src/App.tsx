import { useState } from 'react'
import './App.css'
import SearchBar from './components/SearchBar';
import axios from 'axios';

interface Track {
  id: string;
  title: string;
  artist: string;
  album_art: string | null;       // 640x640 for main display
  album_art_thumb: string | null; // 64x64 for search dropdown
}

interface AudioFeatures {
  energy: number;
  valence: number;
  tempo?: number;
}

export default function App() {
  const [selectedTrack, setSelectedTrack] = useState<Track | null>(null);
  const [audioFeatures, setAudioFeatures] = useState<AudioFeatures | null>(null);
  const [artworkUrl, setArtworkUrl] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('Ready');

  const handleTrackSelect = async (spotifyId: string, track: Track) => {
    setSelectedTrack(track);
    setArtworkUrl(null);
    setError(null);
    setStatus(`Loading features for "${track.title}"...`);
    try {
      const response = await axios.get(`http://localhost:8080/api/v1/soundchart/features/${spotifyId}`);
      setAudioFeatures(response.data.audio_features.audio_features);
      setStatus(`"${track.title}" by ${track.artist} — ready to generate`);
    } catch {
      setError('Could not load audio features.');
      setStatus('Error loading track features');
    }
  };

  const handleGenerateArtwork = async () => {
    if (!audioFeatures) return;
    setIsGenerating(true);
    setArtworkUrl(null);
    setError(null);
    setStatus('Running genetic algorithm...');
    try {
      const response = await axios.post('http://localhost:8080/api/v1/generate-art', {
        energy: audioFeatures.energy,
        valence: audioFeatures.valence,
        density: audioFeatures.tempo ? audioFeatures.tempo / 200 : audioFeatures.energy,
      });
      setArtworkUrl(`http://localhost:8080${response.data.image_url}`);
      setStatus(`Artwork generated for "${selectedTrack?.title}"`);
    } catch {
      setError('Generation failed. Try again.');
      setStatus('Generation failed');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="win98-desktop">
      <div className="win98-window">

        {/* ── Title Bar ── */}
        <div className="win98-titlebar">
          <div className="win98-titlebar-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#ffffff" strokeWidth="2" strokeLinecap="round">
              <path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>
            </svg>
          </div>
          <span className="win98-titlebar-text">Genova — Music Artwork Generator</span>
          <div className="win98-titlebar-buttons">
            <div className="win98-btn-chrome">_</div>
            <div className="win98-btn-chrome">□</div>
            <div className="win98-btn-chrome">✕</div>
          </div>
        </div>

        {/* ── Menu Bar ── */}
        <div className="win98-menubar">
          <span className="win98-menu-item">File</span>
          <span className="win98-menu-item">Edit</span>
          <span className="win98-menu-item">View</span>
          <span className="win98-menu-item">Generate</span>
          <span className="win98-menu-item">Help</span>
        </div>

        {/* ── Body ── */}
        <div className="win98-body">

          {/* Left panel */}
          <div className="panel-left">

            {/* Search section */}
            <div className="panel-section">
              <div style={{ fontSize: 11, fontFamily: 'Arial', marginBottom: 4, color: '#000' }}>
                Track Search:
              </div>
              <SearchBar onSelect={handleTrackSelect} />
            </div>

            {/* Track info groupbox */}
            <div className="panel-section">
              <div className="win98-groupbox">
                <span className="win98-groupbox-label">Track Info</span>
                {selectedTrack ? (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {selectedTrack.album_art ? (
                      <img
                        src={selectedTrack.album_art}
                        alt={selectedTrack.title}
                        className="track-album-thumb"
                      />
                    ) : (
                      <div className="track-album-empty">No image</div>
                    )}
                    <div className="track-title-text">{selectedTrack.title}</div>
                    <div className="track-artist-text">{selectedTrack.artist}</div>
                  </div>
                ) : (
                  <div className="empty-state-text">No track selected</div>
                )}
              </div>
            </div>

            {/* Actions groupbox */}
            <div className="panel-section">
              <div className="win98-groupbox">
                <span className="win98-groupbox-label">Actions</span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6, paddingTop: 4 }}>
                  <button
                    className="win98-push-btn"
                    onClick={handleGenerateArtwork}
                    disabled={!audioFeatures || isGenerating}
                  >
                    {isGenerating ? (
                      <><span className="spinner" /> Generating...</>
                    ) : (
                      '🎨 Generate Artwork'
                    )}
                  </button>
                  {artworkUrl && (
                    <button
                      className="win98-push-btn"
                      onClick={() => { setArtworkUrl(null); setSelectedTrack(null); setAudioFeatures(null); setStatus('Ready'); }}
                    >
                      🗑 Clear
                    </button>
                  )}
                </div>
                {error && <p className="error-msg">{error}</p>}
              </div>
            </div>

          </div>

          {/* Right panel: gallery wall */}
          <div className="panel-right">
            {artworkUrl ? (
              <div className="gallery-scene">
                <div className="ornate-frame">
                  <img
                    src={artworkUrl}
                    alt="Generated artwork"
                    className="gallery-artwork"
                  />
                </div>
                <div className="gallery-placard">
                  <p className="gallery-placard-title">{selectedTrack?.title}</p>
                  <p className="gallery-placard-sub">{selectedTrack?.artist} · Genova · {new Date().getFullYear()}</p>
                </div>
              </div>
            ) : (
              <div className="gallery-empty-scene">
                <div className="ornate-frame-empty">
                  <p className="empty-canvas-text">
                    {isGenerating ? 'Generating…' : 'Awaiting artwork'}
                  </p>
                </div>
                <p className="gallery-empty-label">
                  {isGenerating ? 'Running genetic algorithm...' : 'Select a track and generate to exhibit'}
                </p>
              </div>
            )}
          </div>

        </div>

        {/* ── Status Bar ── */}
        <div className="win98-statusbar">
          <div className="win98-status-panel">{status}</div>
          <div className="win98-status-panel" style={{ flex: 'none', minWidth: 120 }}>
            {selectedTrack ? 'Track loaded' : 'No track'}
          </div>
          <div className="win98-status-panel" style={{ flex: 'none', minWidth: 80 }}>
            Genova v1.0
          </div>
        </div>

      </div>
    </div>
  );
}