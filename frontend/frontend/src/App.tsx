import { useState } from 'react'
import './App.css'
import SearchBar from './components/SearchBar';
import AudioFeaturesPanel from './components/MusicMetrix'
import axios from 'axios';
import type { AudioFeatures } from './components/MusicMetrix';

export default function App() {
  const [audioFeatures, setAudioFeatures] = useState<AudioFeatures | null>(null);
  const [artworkUrl, setArtworkUrl] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [generationProgress, setGenerationProgress] = useState<string>('');

  // 1. Fetches features for the metrics/visual bars
  const handleTrackSelect = async (spotifyId: string) => {
    try {
      // Reset image state when a new song is picked
      setArtworkUrl(null);
      const response = await axios.get(`http://localhost:8080/api/v1/soundchart/features/${spotifyId}`);
      console.log('Soundcharts API JSON Response:', response.data);
      setAudioFeatures(response.data.audio_features.audio_features);
    } catch (err) {
      console.error('Failed to fetch audio features', err);
    }
  };

  // 2. Transmits local features down to the stateless art generator
  const handleGenerateArtwork = async () => {
    if (!audioFeatures) return;

    setIsGenerating(true);
    setArtworkUrl(null);

    // Initialize raw native browser WebSocket connection
    const ws = new WebSocket('ws://localhost:8080/api/v1/ws/generate-art');

    ws.onopen = () => {
      // Send configurations to initiate backend loop processing
      ws.send(JSON.stringify({
        energy: audioFeatures.energy,
        valence: audioFeatures.valence,
        density: audioFeatures.tempo ? audioFeatures.tempo / 200 : audioFeatures.energy
      }));
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'generation_frame') {
        setGenerationProgress(`Evolving Canvas: Generation ${data.generation}/${data.total_generations}`);
        // Swap out preview immediately using streaming base64 text injection
        setArtworkUrl(data.frame);
      }

      else if (data.type === 'final_result') {
        setGenerationProgress('Evolution complete! Rendered final high-res canvas.');
        // Lock in final saved image disk static routing path
        setArtworkUrl(`http://localhost:8080${data.image_url}`);
        ws.close();
      }

      else if (data.type === 'error') {
        console.error('GA Engine Error:', data.message);
        ws.close();
      }
    };

    ws.onclose = () => {
      setIsGenerating(false);
    };

    ws.onerror = (error) => {
      console.error('WebSocket Exception occurred:', error);
      setIsGenerating(false);
    };
  };

  return (
    <div style={{ display: 'flex', height: '100vh', backgroundColor: '#16171d', color: '#f3f4f6' }}>
      {/* Left panel */}
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
              {isGenerating ? 'Evolving Live via GA...' : 'Generate Musical Artwork'}
            </button>
          </div>
        )}
      </div>

      {/* Right panel */}
      <div style={{ width: '50%', padding: '2rem', display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column' }}>
        {artworkUrl ? (
          <div style={{ textAlign: 'center' }}>
            <img
              src={artworkUrl}
              alt="Evolved Fluid Canvas"
              style={{
                width: '400px',
                height: '400px',
                objectFit: 'cover',
                borderRadius: '12px',
                boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)',
                border: isGenerating ? '2px solid #c084fc' : 'none'
              }}
            />
            <p style={{ marginTop: '1rem', color: '#c084fc', fontSize: '14px', fontWeight: '500' }}>
              {generationProgress}
            </p>
          </div>
        ) : (
          <div style={{ color: '#6b6375', textAlign: 'center' }}>
            <p>Select a track and generate art to watch the real-time visual evolution wrapper.</p>
          </div>
        )}
      </div>
    </div>
  );
}