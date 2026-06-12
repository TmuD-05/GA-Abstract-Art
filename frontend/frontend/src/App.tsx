import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import SearchBar from './components/SearchBar';
import AudioFeaturesPanel from './components/MusicMetrix'
import axios from 'axios';
import type { AudioFeatures } from './components/MusicMetrix';

export default function App() {
  const [audioFeatures, setAudioFeatures] = useState<AudioFeatures | null>(null);
  const [artworkUrl, setArtworkUrl] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);

  // 1. Fetches features for the metrics/visual bars
  const handleTrackSelect = async (spotifyId: string) => {
    try {
      // Reset image state when a new song is picked
      setArtworkUrl(null);
      const response = await axios.get(`http://localhost:8080/api/v1/soundchart/features/${spotifyId}`);
      setAudioFeatures(response.data.audio_features);
    } catch (err) {
      console.error('Failed to fetch audio features', err);
    }
  };

  // 2. Transmits local features down to the stateless art generator
  const handleGenerateArtwork = async () => {
    if (!audioFeatures) return;

    setIsGenerating(true);
    try {
      const response = await axios.post('http://localhost:8080/api/v1/generate-art', {
        energy: audioFeatures.energy,
        valence: audioFeatures.valence,
        // Fallback to energy if density is missing from the payload
        density: audioFeatures.tempo ? audioFeatures.tempo / 200 : audioFeatures.energy 
      });

      if (response.data.success) {
        // Build absolute asset path using the server prefix + absolute static directory route
        setArtworkUrl(`http://localhost:8080${response.data.image_url}`);
      }
    } catch (err) {
      console.error('Failed to generate abstract image canvas', err);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', backgroundColor: '#16171d', color: '#f3f4f6' }}>
      {/* Left panel: Search and metric bars */}
      <div style={{ width: '50%', padding: '2rem', borderRight: '1px solid #2e303a', overflowY: 'auto' }}>
        <SearchBar onSelect={handleTrackSelect} />
        
        {audioFeatures && (
          <div style={{ marginTop: '2rem' }}>
            <AudioFeaturesPanel features={audioFeatures} />
            
            <button 
              onClick={handleGenerateArtwork}
              disabled={isGenerating}
              style={{
                marginTop: '2rem',
                padding: '12px 24px',
                fontSize: '16px',
                fontWeight: 'bold',
                borderRadius: '6px',
                border: 'none',
                backgroundColor: isGenerating ? '#4b5563' : '#c084fc',
                color: '#16171d',
                cursor: isGenerating ? 'not-allowed' : 'pointer',
                transition: 'background-color 0.2s'
              }}
            >
              {isGenerating ? 'Evolving Canvas via GA...' : 'Generate Musical Artwork'}
            </button>
          </div>
        )}
      </div>

      {/* Right panel: Live Generated Artwork Display */}
      <div style={{ width: '50%', padding: '2rem', display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column' }}>
        {artworkUrl ? (
          <div style={{ textAlign: 'center' }}>
            <img 
              src={artworkUrl} 
              alt="Evolved Fluid Canvas" 
              style={{ 
                maxWidth: '100%', 
                maxHeight: '75vh', 
                borderRadius: '12px', 
                boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)' 
              }} 
            />
            <p style={{ marginTop: '1rem', color: '#9ca3af', fontSize: '14px' }}>
              Successfully rendered via Genetic Algorithm Domain Warping
            </p>
          </div>
        ) : (
          <div style={{ color: '#6b6375', textAlign: 'center' }}>
            {isGenerating ? (
              <p style={{ color: '#c084fc', fontSize: '18px' }}>Running iterations across generations...</p>
            ) : (
              <p>Select a track and generate art to view the fluid canvas visualization.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}