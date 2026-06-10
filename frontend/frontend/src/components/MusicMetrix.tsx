export interface AudioFeatures {
  acousticness: number;
  danceability: number;
  energy: number;
  instrumentalness: number;
  key: number;
  liveness: number;
  loudness: number;
  mode: number;
  speechiness: number;
  tempo: number;
  timeSignature: number;
  valence: number;
}

interface Props {
  features: AudioFeatures;
}

export default function AudioFeaturesPanel({ features }: Props) {
  return (
    <div>
      {Object.entries(features).map(([key, val]) => (
        <div key={key}>
          <span>{key}: </span>
          <span>{typeof val === 'number' ? val.toFixed(2) : String(val)}</span>
        </div>
      ))}
    </div>
  );
}